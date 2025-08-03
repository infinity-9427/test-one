"""
Cloudinary API endpoints for screenshot upload and management.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any
import os
import tempfile

from ..services.cloudinary import cloudinary_service

router = APIRouter(prefix="/api/v1/cloudinary", tags=["cloudinary"])


@router.post("/upload")
async def upload_screenshot(
    file: UploadFile = File(...),
    url: str = "",
    viewport_type: str = "desktop"
):
    """
    Upload screenshot to Cloudinary.
    
    Args:
        file: Screenshot file to upload
        url: Original website URL
        viewport_type: desktop or mobile
        
    Returns:
        Upload result with Cloudinary URLs
    """
    try:
        if not cloudinary_service.is_configured():
            raise HTTPException(status_code=503, detail="Cloudinary service not configured")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Prepare screenshot data
            screenshot_data = {
                "url": url,
                "viewport_type": viewport_type,
                "viewport": {"width": 1200, "height": 800} if viewport_type == "desktop" else {"width": 375, "height": 667},
                "page_metrics": {"title": "Manual Upload"},
                "captured_at": "manual"
            }
            
            # Upload to Cloudinary
            upload_result = await cloudinary_service.upload_screenshot(
                temp_file_path,
                screenshot_data
            )
            
            return {
                "success": True,
                "cloudinary_url": upload_result.get("cloudinary_url"),
                "thumbnail_url": upload_result.get("cloudinary_thumbnail"),
                "public_id": upload_result.get("cloudinary_public_id"),
                "file_size": upload_result.get("file_size"),
                "format": upload_result.get("format")
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/health")
async def cloudinary_health():
    """Check Cloudinary service health."""
    try:
        is_configured = cloudinary_service.is_configured()
        connection_test = await cloudinary_service.test_connection() if is_configured else False
        
        return {
            "status": "healthy" if (is_configured and connection_test) else "unhealthy",
            "configured": is_configured,
            "connection_test": connection_test,
            "service": "cloudinary"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "cloudinary"
        }


@router.delete("/delete/{public_id}")
async def delete_screenshot(public_id: str):
    """Delete screenshot from Cloudinary."""
    try:
        if not cloudinary_service.is_configured():
            raise HTTPException(status_code=503, detail="Cloudinary service not configured")
        
        success = await cloudinary_service.delete_screenshot(public_id)
        
        if success:
            return {"success": True, "message": "Screenshot deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Screenshot not found or deletion failed")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


@router.get("/thumbnail/{public_id}")
async def get_thumbnail_url(public_id: str, width: int = 300, height: int = 200):
    """Generate thumbnail URL for a screenshot."""
    try:
        if not cloudinary_service.is_configured():
            raise HTTPException(status_code=503, detail="Cloudinary service not configured")
        
        thumbnail_url = cloudinary_service.get_thumbnail_url(public_id, width, height)
        
        if thumbnail_url:
            return {"thumbnail_url": thumbnail_url}
        else:
            raise HTTPException(status_code=404, detail="Could not generate thumbnail URL")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Thumbnail generation failed: {str(e)}")
