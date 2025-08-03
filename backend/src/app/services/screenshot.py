"""
Screenshot capture service using Playwright.
Supports desktop and mobile viewports with error handling and caching.
"""
import asyncio
import hashlib
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Browser, Page
from PIL import Image
import aiofiles

from ..core.settings import settings


class ScreenshotCache:
    """Simple file-based TTL cache for screenshots."""
    
    def __init__(self, cache_dir: str, ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, url: str, viewport: Dict[str, int]) -> str:
        """Generate cache key from URL and viewport."""
        content = f"{url}_{viewport['width']}x{viewport['height']}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{cache_key}.json"
    
    async def get(self, url: str, viewport: Dict[str, int]) -> Optional[Dict[str, Any]]:
        """Get cached screenshot data if valid."""
        try:
            cache_key = self._get_cache_key(url, viewport)
            cache_path = self._get_cache_path(cache_key)
            
            if not cache_path.exists():
                return None
            
            async with aiofiles.open(cache_path, 'r') as f:
                cache_data = json.loads(await f.read())
            
            # Check TTL
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=self.ttl_hours):
                # Cache expired, remove file
                cache_path.unlink(missing_ok=True)
                return None
            
            # Verify screenshot file still exists
            screenshot_path = Path(cache_data['local_path'])
            if not screenshot_path.exists():
                cache_path.unlink(missing_ok=True)
                return None
            
            return cache_data
            
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    async def set(self, url: str, viewport: Dict[str, int], screenshot_data: Dict[str, Any]) -> None:
        """Cache screenshot data."""
        try:
            cache_key = self._get_cache_key(url, viewport)
            cache_path = self._get_cache_path(cache_key)
            
            cache_data = {
                **screenshot_data,
                'timestamp': datetime.now().isoformat(),
                'cache_key': cache_key
            }
            
            async with aiofiles.open(cache_path, 'w') as f:
                await f.write(json.dumps(cache_data))
                
        except Exception as e:
            print(f"Cache set error: {e}")


class ScreenshotService:
    """Screenshot capture service with Playwright."""
    
    # Standard viewports
    DESKTOP_VIEWPORT = {"width": 1200, "height": 800}
    MOBILE_VIEWPORT = {"width": 375, "height": 667}
    
    def __init__(self):
        self.cache = ScreenshotCache(
            cache_dir=settings.cache_dir,
            ttl_hours=settings.cache_ttl_hours
        ) if settings.cache_enabled else None
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    async def _capture_screenshot_with_playwright(
        self, 
        url: str, 
        viewport: Dict[str, int],
        timeout: Optional[int] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Capture screenshot using Playwright."""
        timeout = timeout or settings.playwright_timeout
        
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(
                    headless=settings.playwright_headless,
                    args=['--no-sandbox', '--disable-dev-shm-usage']  # For better compatibility
                )
                
                try:
                    # Create page with viewport
                    page = await browser.new_page(viewport={
                        "width": viewport["width"],
                        "height": viewport["height"]
                    })
                    
                    # Set timeout
                    page.set_default_timeout(timeout)
                    
                    # Navigate to URL
                    try:
                        response = await page.goto(url, wait_until='networkidle')
                        
                        if not response:
                            raise Exception("Failed to load page - no response")
                        
                        if response.status >= 400:
                            raise Exception(f"HTTP {response.status} - {response.status_text}")
                    
                    except Exception as nav_error:
                        raise Exception(f"Navigation failed: {str(nav_error)}")
                    
                    # Wait for page to be fully loaded
                    await page.wait_for_load_state('networkidle')
                    
                    # Take screenshot
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}_{viewport['width']}x{viewport['height']}.png"
                    local_path = self.cache.cache_dir / filename if self.cache else Path(f"./screenshots/{filename}")
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    screenshot_bytes = await page.screenshot(
                        path=str(local_path),
                        full_page=True,
                        type='png'
                    )
                    
                    # Get page title and basic metrics
                    title = await page.title()
                    
                    # Get basic page metrics
                    page_metrics = {
                        "title": title,
                        "url": page.url,
                        "viewport": viewport,
                        "screenshot_size": len(screenshot_bytes),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return str(local_path), page_metrics
                    
                finally:
                    await browser.close()
                    
        except Exception as e:
            raise Exception(f"Screenshot capture failed: {str(e)}")
    
    async def capture_screenshot(
        self, 
        url: str, 
        viewport_type: str = "desktop"
    ) -> Dict[str, Any]:
        """
        Capture screenshot of a website.
        
        Args:
            url: Website URL to capture
            viewport_type: "desktop" or "mobile"
            
        Returns:
            Dictionary with screenshot data and metadata
        """
        try:
            # Validate URL
            if not self._validate_url(url):
                raise ValueError(f"Invalid URL format: {url}")
            
            # Get viewport
            viewport = self.DESKTOP_VIEWPORT if viewport_type == "desktop" else self.MOBILE_VIEWPORT
            
            # Check cache first
            if self.cache:
                cached_data = await self.cache.get(url, viewport)
                if cached_data:
                    return {
                        **cached_data,
                        "from_cache": True
                    }
            
            # Capture new screenshot
            local_path, page_metrics = await self._capture_screenshot_with_playwright(url, viewport)
            
            result = {
                "url": url,
                "viewport_type": viewport_type,
                "viewport": viewport,
                "local_path": local_path,
                "page_metrics": page_metrics,
                "from_cache": False,
                "captured_at": datetime.now().isoformat()
            }
            
            # Cache the result
            if self.cache:
                await self.cache.set(url, viewport, result)
            
            return result
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Screenshot service error: {str(e)}")
    
    async def capture_both_viewports(self, url: str) -> Dict[str, Any]:
        """
        Capture screenshots for both desktop and mobile viewports.
        
        Args:
            url: Website URL to capture
            
        Returns:
            Dictionary with both desktop and mobile screenshots
        """
        try:
            # Capture both viewports concurrently
            desktop_task = asyncio.create_task(self.capture_screenshot(url, "desktop"))
            mobile_task = asyncio.create_task(self.capture_screenshot(url, "mobile"))
            
            desktop_result, mobile_result = await asyncio.gather(
                desktop_task, 
                mobile_task,
                return_exceptions=True
            )
            
            result = {
                "url": url,
                "captured_at": datetime.now().isoformat(),
                "desktop": None,
                "mobile": None,
                "errors": {}
            }
            
            # Process desktop result
            if isinstance(desktop_result, Exception):
                result["errors"]["desktop"] = str(desktop_result)
            else:
                result["desktop"] = desktop_result
            
            # Process mobile result
            if isinstance(mobile_result, Exception):
                result["errors"]["mobile"] = str(mobile_result)
            else:
                result["mobile"] = mobile_result
            
            # Check if we have at least one successful capture
            if not result["desktop"] and not result["mobile"]:
                raise Exception(f"Failed to capture both viewports: {result['errors']}")
            
            return result
            
        except Exception as e:
            raise Exception(f"Multi-viewport capture failed: {str(e)}")


# Global service instance
screenshot_service = ScreenshotService()
