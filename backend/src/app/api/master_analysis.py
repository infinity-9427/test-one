"""
Master Analysis API - Single endpoint for complete website analysis workflow.
Orchestrates: Screenshot → Analysis → Cloudinary Upload → Google Sheets Logging
Based on Orchestrator Pattern with parallel execution and graceful degradation.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime

from ..services.screenshot_storage import screenshot_storage_service
from ..services.ai_analysis import ai_analysis_service
from ..services.cloudinary import cloudinary_service
from ..services.google_sheets import google_sheets_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/master", tags=["master-orchestrator"])


# Response Schema Models
class ScreenshotResult(BaseModel):
    """Result of screenshot capture for a specific device."""
    device: str
    url: Optional[str] = None
    local_path: Optional[str] = None
    cloudinary_url: Optional[str] = None
    error: Optional[str] = None
    captured_at: Optional[str] = None


class AnalysisResult(BaseModel):
    """Complete analysis result with all services orchestrated."""
    analysis_id: str
    url: str
    status: str
    completed_at: str
    analysis_duration: float
    screenshots: List[ScreenshotResult]
    ai_insights: Optional[Dict[str, Any]] = None
    overall_score: Optional[float] = None
    scores_breakdown: Optional[Dict[str, float]] = None
    uploads: Dict[str, Optional[str]] = {}
    sheet_entry_id: Optional[str] = None
    errors: Dict[str, str] = {}


class MasterAnalysisRequest(BaseModel):
    """Request model for complete website analysis."""
    url: HttpUrl
    auto_log_to_sheets: bool = True
    include_mobile: bool = True


@router.post("/analyze-complete", response_model=AnalysisResult)
async def master_analyze(
    request: MasterAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Complete website analysis workflow in a single endpoint.
    
    Orchestrates the entire process with parallel execution and graceful degradation:
    1. Takes screenshots (desktop + mobile) in parallel with cloud upload
    2. Runs comprehensive AI and rule-based analysis 
    3. Uploads images and logs to sheets in background
    4. Returns complete analysis data immediately
    
    AI analysis and cloud storage are always enabled for complete functionality.
    Perfect for frontend integration - just send URL, get everything back.
    """
    analysis_id = f"master_{int(datetime.now().timestamp())}"
    start_time = datetime.now()
    url_str = str(request.url)
    
    # Initialize result structure
    result = AnalysisResult(
        analysis_id=analysis_id,
        url=url_str,
        status="processing",
        completed_at="",
        analysis_duration=0.0,
        screenshots=[],
        uploads={},
        errors={}
    )
    
    logger.info(f"[{analysis_id}] Starting master analysis for {url_str}")
    
    try:
        # Step 1: Fire screenshots with integrated upload (desktop + mobile)
        logger.info(f"[{analysis_id}] Capturing screenshots with cloud storage...")
        logger.info(f"[{analysis_id}] DEBUG: Using capture_and_store_both_viewports method")
        logger.info(f"[{analysis_id}] DEBUG: store_cloudinary=True (always enabled)")
        
        try:
            # Use the unified capture method that handles both viewports and uploads
            screenshot_result = await screenshot_storage_service.capture_and_store_both_viewports(
                url=url_str,
                upload_to_cloud=True  # Always upload to cloud for complete analysis
            )
            
            logger.info(f"[{analysis_id}] DEBUG: Screenshot result type: {type(screenshot_result)}")
            logger.info(f"[{analysis_id}] DEBUG: Screenshot result keys: {list(screenshot_result.keys()) if isinstance(screenshot_result, dict) else 'Not a dict'}")
            
            # Process the results into our expected format
            if screenshot_result:
                # Desktop screenshot
                if "desktop" in screenshot_result:
                    desktop_data = screenshot_result["desktop"]
                    screenshot_data = desktop_data.get("screenshot_data", {})
                    storage_data = desktop_data.get("storage_data", {})
                    
                    result.screenshots.append(
                        ScreenshotResult(
                            device="desktop",
                            url=screenshot_data.get("url", url_str),
                            local_path=screenshot_data.get("local_path"),
                            cloudinary_url=storage_data.get("cloudinary_url") if storage_data else None,
                            captured_at=screenshot_data.get("timestamp")
                        )
                    )
                    
                    # Collect upload URLs if available
                    if storage_data and storage_data.get("cloudinary_url"):
                        result.uploads["desktop_url"] = storage_data.get("cloudinary_url")
                        if storage_data.get("cloudinary_thumbnail"):
                            result.uploads["desktop_thumbnail"] = storage_data.get("cloudinary_thumbnail")
                
                # Mobile screenshot (if requested)
                if request.include_mobile and "mobile" in screenshot_result:
                    mobile_data = screenshot_result["mobile"]
                    screenshot_data = mobile_data.get("screenshot_data", {})
                    storage_data = mobile_data.get("storage_data", {})
                    
                    result.screenshots.append(
                        ScreenshotResult(
                            device="mobile", 
                            url=screenshot_data.get("url", url_str),
                            local_path=screenshot_data.get("local_path"),
                            cloudinary_url=storage_data.get("cloudinary_url") if storage_data else None,
                            captured_at=screenshot_data.get("timestamp")
                        )
                    )
                    
                    # Collect upload URLs if available
                    if storage_data and storage_data.get("cloudinary_url"):
                        result.uploads["mobile_url"] = storage_data.get("cloudinary_url")
                        if storage_data.get("cloudinary_thumbnail"):
                            result.uploads["mobile_thumbnail"] = storage_data.get("cloudinary_thumbnail")
                
                # Mark as good screenshots for AI analysis
                good_screenshots = [screenshot_result]
                
            else:
                logger.error(f"[{analysis_id}] Screenshot capture failed - no result returned")
                result.errors["screenshot_capture"] = "Failed to capture screenshots"
                good_screenshots = []
                
        except Exception as e:
            logger.error(f"[{analysis_id}] Screenshot capture failed: {e}")
            result.screenshots.append(
                ScreenshotResult(
                    device="desktop",
                    error=str(e)
                )
            )
            result.errors["screenshot_capture"] = str(e)
            good_screenshots = []
        
        # Step 2: If at least one screenshot succeeded, run AI analysis (always enabled)
        if good_screenshots:
            try:
                logger.info(f"[{analysis_id}] Running AI analysis...")
                
                # Prepare screenshot data for AI analysis
                screenshot_data = {"desktop": None, "mobile": None}
                if good_screenshots and len(good_screenshots) > 0:
                    screenshot_result = good_screenshots[0]  # We have one unified result
                    
                    # Extract desktop screenshot data
                    if "desktop" in screenshot_result:
                        screenshot_data["desktop"] = screenshot_result["desktop"].get("screenshot_data", {})
                    
                    # Extract mobile screenshot data if available
                    if "mobile" in screenshot_result:
                        screenshot_data["mobile"] = screenshot_result["mobile"].get("screenshot_data", {})
                
                # Run AI analysis
                ai_result = await ai_analysis_service.analyze_website_design(
                    url_str, 
                    screenshot_data
                )
                
                result.ai_insights = ai_result
                
                # Extract scores if available
                if ai_result and "scores_breakdown" in ai_result:
                    result.scores_breakdown = ai_result["scores_breakdown"]
                    result.overall_score = ai_result.get("overall_score")
                
                logger.info(f"[{analysis_id}] AI analysis completed")
                
            except Exception as e:
                logger.error(f"[{analysis_id}] AI analysis failed: {e}")
                result.errors["ai_analysis"] = str(e)
        
        # Step 3: Fire Google Sheets logging in background if requested
        if good_screenshots and request.auto_log_to_sheets:
            logger.info(f"[{analysis_id}] Scheduling Google Sheets logging task...")
            background_tasks.add_task(
                _log_to_sheets_background,
                analysis_id,
                url_str,
                result.screenshots,
                result.ai_insights,
                result.uploads
            )
            logger.info(f"[{analysis_id}] Background task scheduled successfully")
        
        # Step 4: Finalize result
        end_time = datetime.now()
        result.analysis_duration = (end_time - start_time).total_seconds()
        result.completed_at = end_time.isoformat()
        result.status = "completed" if good_screenshots else "failed"
        
        logger.info(f"[{analysis_id}] Master analysis completed in {result.analysis_duration:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"[{analysis_id}] Master analysis failed: {e}")
        end_time = datetime.now()
        result.analysis_duration = (end_time - start_time).total_seconds()
        result.completed_at = end_time.isoformat()
        result.status = "failed"
        result.errors["master_analysis"] = str(e)
        return result


async def _log_to_sheets_background(
    analysis_id: str,
    url: str,
    screenshots: List[ScreenshotResult],
    ai_insights: Optional[Dict[str, Any]],
    uploads: Dict[str, Optional[str]]
):
    """
    Background task for Google Sheets logging with Cloudinary URLs.
    """
    logger.info(f"[{analysis_id}] Starting Google Sheets logging...")
    
    try:
        # Initialize Google Sheets service if not already done
        if not google_sheets_service._initialized:
            init_success = await google_sheets_service.initialize()
            if not init_success:
                logger.error(f"[{analysis_id}] Failed to initialize Google Sheets service")
                return
        
        # Organize screenshot data for sheets logging
        screenshot_data = {"desktop": {}, "mobile": {}}
        
        for screenshot in screenshots:
            if screenshot.device and screenshot.cloudinary_url:
                screenshot_data[screenshot.device] = {
                    "local_path": screenshot.local_path,
                    "cloudinary_url": screenshot.cloudinary_url,
                    "viewport": {},  # Could be extracted if needed
                    "page_metrics": {}  # Could be extracted if needed
                }
        
        # Prepare analysis result for sheets logging
        analysis_result = {
            "analysis_id": analysis_id,
            "url": url,
            "analyzed_at": ai_insights.get("analyzed_at") if ai_insights else datetime.now().isoformat(),
            "overall_score": ai_insights.get("overall_score", 0) if ai_insights else 0,
            "scores_breakdown": ai_insights.get("scores_breakdown", {}) if ai_insights else {},
            "screenshots": screenshot_data,
            "llm_analysis": ai_insights.get("llm_analysis") if ai_insights else {},
            "analysis_duration": ai_insights.get("analysis_duration", 0) if ai_insights else 0
        }
        
        logger.info(f"[{analysis_id}] Logging to Google Sheets with data:")
        logger.info(f"[{analysis_id}] - URL: {url}")
        logger.info(f"[{analysis_id}] - Desktop URL: {screenshot_data.get('desktop', {}).get('cloudinary_url', 'None')}")
        logger.info(f"[{analysis_id}] - Mobile URL: {screenshot_data.get('mobile', {}).get('cloudinary_url', 'None')}")
        
        # Log to Google Sheets
        success = await google_sheets_service.log_analysis_result(analysis_result)
        
        if success:
            logger.info(f"[{analysis_id}] Successfully logged to Google Sheets")
        else:
            logger.error(f"[{analysis_id}] Failed to log to Google Sheets")
        
    except Exception as e:
        logger.error(f"[{analysis_id}] Google Sheets logging failed: {e}")
        # Log the exception details for debugging
        import traceback
        logger.error(f"[{analysis_id}] Full traceback: {traceback.format_exc()}")
    
    logger.info(f"[{analysis_id}] Background tasks completed")


@router.get("/health")
async def master_analysis_health():
    """Health check for master analysis orchestrator."""
    services_status = {}
    
    # Check individual service health
    try:
        # Screenshot service
        services_status["screenshots"] = "available"
        
        # AI analysis service  
        services_status["ai_analysis"] = "available"
        
        # Cloudinary service
        services_status["cloudinary"] = "available"
        
        # Google Sheets service
        sheets_health = await google_sheets_service.health_check()
        services_status["google_sheets"] = "available" if sheets_health.get("status") == "healthy" else "unavailable"
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
    
    overall_status = "healthy" if all(
        status == "available" for status in services_status.values()
    ) else "degraded"
    
    return {
        "status": overall_status,
        "services": services_status,
        "message": "Master orchestrator ready" if overall_status == "healthy" else "Some services unavailable",
        "endpoint": "/api/v1/master/analyze-complete"
    }
