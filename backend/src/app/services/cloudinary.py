"""
Cloudinary storage service for screenshot upload and management.
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional

import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

from ..core.settings import settings


class CloudinaryService:
    """Cloudinary image storage and management service."""
    
    def __init__(self):
        self._configure_cloudinary()
    
    def _configure_cloudinary(self) -> None:
        """Configure Cloudinary with credentials."""
        try:
            if not all([
                settings.cloudinary_cloud_name,
                settings.cloudinary_api_key,
                settings.cloudinary_api_secret
            ]):
                print("Warning: Cloudinary credentials not configured")
                self.configured = False
                return
            
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True
            )
            
            self.configured = True
            print("Cloudinary configured successfully")
            
        except Exception as e:
            print(f"Cloudinary configuration error: {e}")
            self.configured = False
    
    def is_configured(self) -> bool:
        """Check if Cloudinary is properly configured."""
        return self.configured
    
    async def upload_screenshot(
        self, 
        file_path: str, 
        screenshot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Upload screenshot to Cloudinary.
        
        Args:
            file_path: Local path to screenshot file
            screenshot_data: Screenshot metadata
            
        Returns:
            Upload result with Cloudinary URLs and metadata
        """
        try:
            if not self.configured:
                raise Exception("Cloudinary not configured. Please provide API credentials.")
            
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Screenshot file not found: {file_path}")
            
            # Generate public ID and tags
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            viewport_type = screenshot_data.get("viewport_type", "unknown")
            public_id = f"website-screenshots/{timestamp}_{viewport_type}"
            
       
            tags = [
                "design-analysis",  
                f"viewport-{viewport_type}",  # desktop/mobile
                timestamp.split("_")[0],  # date: 20250802
                "unscored"  # Will be updated to scoring category after analysis
            ]
            
            # Add URL domain as tag if available
            url = screenshot_data.get("url", "")
            if url:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc.replace("www.", "")
                    if domain:
                        tags.append(f"domain-{domain}")
                except:
                    pass
            
            # Upload to Cloudinary with optimizations
            upload_result = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                tags=tags,
                resource_type="image",
                format="webp",  # Convert to WebP for better compression
                folder=settings.upload_folder,  # Use UPLOAD_FOLDER from .env
                quality="auto",  # Automatic quality optimization
                fetch_format="auto",  # Automatic format selection
                transformation=[
                    {'width': 1200, 'crop': "limit"},  # Limit max width to 1200px
                    {'height': 1200, 'crop': "limit"},  # Limit max height to 1200px  
                    {'quality': "auto"},  # Auto quality
                    {'fetch_format': "auto"}  # Auto format
                ],
                context={
                    "url": screenshot_data.get("url", ""),
                    "viewport": f"{screenshot_data.get('viewport', {}).get('width', 0)}x{screenshot_data.get('viewport', {}).get('height', 0)}",
                    "captured_at": screenshot_data.get("captured_at", ""),
                    "title": screenshot_data.get("page_metrics", {}).get("title", "")
                }
            )
            
            return {
                "cloudinary_public_id": upload_result["public_id"],
                "cloudinary_url": upload_result["secure_url"],
                "cloudinary_thumbnail": cloudinary.CloudinaryImage(upload_result["public_id"]).build_url(
                    width=300, height=200, crop="fill", quality="auto", fetch_format="auto"
                ),
                "upload_timestamp": datetime.now().isoformat(),
                "file_size": upload_result.get("bytes", 0),
                "format": upload_result.get("format", "webp"),  # Updated to webp
                "tags": tags,
                "optimized": True  # Flag to indicate optimizations applied
            }
            
        except CloudinaryError as e:
            raise Exception(f"Cloudinary upload failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Screenshot upload error: {str(e)}")
    
    async def delete_screenshot(self, public_id: str) -> bool:
        """
        Delete screenshot from Cloudinary.
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            True if deletion successful
        """
        try:
            if not self.configured:
                raise Exception("Cloudinary not configured")
            
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
            
        except Exception as e:
            print(f"Screenshot deletion error: {e}")
            return False
    
    def get_thumbnail_url(self, public_id: str, width: int = 300, height: int = 200) -> str:
        """
        Generate optimized thumbnail URL for a screenshot.
        
        Args:
            public_id: Cloudinary public ID
            width: Thumbnail width
            height: Thumbnail height
            
        Returns:
            Optimized thumbnail URL
        """
        try:
            if not self.configured:
                return ""
            
            return cloudinary.CloudinaryImage(public_id).build_url(
                width=width, 
                height=height, 
                crop="fill", 
                quality="auto",
                fetch_format="auto"  # Auto format optimization
            )
            
        except Exception as e:
            print(f"Thumbnail URL generation error: {e}")
            return ""


# Global service instance
cloudinary_service = CloudinaryService()
