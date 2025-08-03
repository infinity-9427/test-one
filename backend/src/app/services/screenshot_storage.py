
from typing import Dict, Any, Optional
from datetime import datetime

from .screenshot import screenshot_service
from .cloudinary import cloudinary_service


class ScreenshotStorageService:
    
    def __init__(self):
        self.screenshot_service = screenshot_service
        self.cloudinary_service = cloudinary_service
    
    async def capture_and_store(
        self, 
        url: str, 
        viewport_type: str = "desktop",
        upload_to_cloud: bool = True
    ) -> Dict[str, Any]:

        try:
            # Capture screenshot
            screenshot_data = await self.screenshot_service.capture_screenshot(url, viewport_type)
            
            result = {
                "url": url,
                "viewport_type": viewport_type,
                "screenshot_data": screenshot_data,
                "storage_data": None
            }
            
            # Upload to cloud if requested and configured
            if upload_to_cloud:
                if not self.cloudinary_service.is_configured():
                    raise Exception("Cloud storage requested but Cloudinary is not configured")
                
                storage_data = await self.cloudinary_service.upload_screenshot(
                    screenshot_data["local_path"],
                    screenshot_data
                )
                result["storage_data"] = storage_data
            
            return result
            
        except Exception as e:
            print(f"Screenshot capture and storage failed for {url}: {e}")
            raise Exception("We're experiencing issues with screenshot capture and storage. Please try again later.")
    
    async def capture_and_store_both_viewports(
        self, 
        url: str,
        upload_to_cloud: bool = True
    ) -> Dict[str, Any]:
        try:
            # Capture both viewports
            screenshots = await self.screenshot_service.capture_both_viewports(url)
            
            result = {
                "url": url,
                "captured_at": datetime.now().isoformat(),
                "desktop": None,
                "mobile": None
            }
            
            # Process desktop screenshot
            if screenshots.get("desktop"):
                desktop_result = {
                    "screenshot_data": screenshots["desktop"],
                    "storage_data": None
                }
                
                if upload_to_cloud:
                    if not self.cloudinary_service.is_configured():
                        raise Exception("Cloud storage requested but Cloudinary is not configured")
                    
                    storage_data = await self.cloudinary_service.upload_screenshot(
                        screenshots["desktop"]["local_path"],
                        screenshots["desktop"]
                    )
                    desktop_result["storage_data"] = storage_data
                
                result["desktop"] = desktop_result
            
            # Process mobile screenshot
            if screenshots.get("mobile"):
                mobile_result = {
                    "screenshot_data": screenshots["mobile"],
                    "storage_data": None
                }
                
                if upload_to_cloud:
                    if not self.cloudinary_service.is_configured():
                        raise Exception("Cloud storage requested but Cloudinary is not configured")
                    
                    storage_data = await self.cloudinary_service.upload_screenshot(
                        screenshots["mobile"]["local_path"],
                        screenshots["mobile"]
                    )
                    mobile_result["storage_data"] = storage_data
                
                result["mobile"] = mobile_result
            
            return result
            
        except Exception as e:
            print(f"Multi-viewport capture and storage failed for {url}: {e}")
            raise Exception("We're experiencing issues with screenshot capture and storage. Please try again later.")


# Global service instance
screenshot_storage_service = ScreenshotStorageService()
