"""
Screenshot capture API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any
from datetime import datetime

from ..services.screenshot_storage import screenshot_storage_service


class ScreenshotRequest(BaseModel):
    url: HttpUrl = Field(..., description="Website URL to capture")
    upload_to_cloud: bool = Field(default=True, description="Upload to cloud storage")
    capture_mode: str = Field(default="viewport", description="Capture mode: 'viewport' for consistent dimensions, 'full_page' for variable height")


class ScreenshotResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime


router = APIRouter(tags=["Screenshots"])


@router.post("/capture", response_model=ScreenshotResponse)
async def capture_screenshots(request: ScreenshotRequest):

    try:
        # Set capture mode based on request
        if request.capture_mode in ["viewport", "full_page"]:
            screenshot_storage_service.screenshot_service.set_capture_mode(request.capture_mode)
        
        # Capture both viewports
        result = await screenshot_storage_service.capture_and_store_both_viewports(
            url=str(request.url),
            upload_to_cloud=request.upload_to_cloud
        )
        
        return ScreenshotResponse(
            success=True,
            data=result,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="We're experiencing technical difficulties with screenshot capture. Please try again later."
        )
