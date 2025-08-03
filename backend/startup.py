#!/usr/bin/env python3
"""
Startup script for Website Design Scorer Backend.
Initializes all services and runs health checks before starting the main application.
"""
import asyncio
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from src.app.core.settings import settings
from src.app.services.google_sheets import google_sheets_service
from src.app.services.cloudinary import cloudinary_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_services():
    """Initialize all required services and perform health checks."""
    logger.info("🚀 Starting Website Design Scorer Backend...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Check Cloudinary configuration
    logger.info("🔍 Checking Cloudinary configuration...")
    if cloudinary_service.is_configured():
        logger.info("✅ Cloudinary: Configured")
        # Test connection
        cloudinary_test = await cloudinary_service.test_connection()
        if cloudinary_test:
            logger.info("✅ Cloudinary: Connection test successful")
        else:
            logger.warning("⚠️ Cloudinary: Connection test failed")
    else:
        logger.warning("⚠️ Cloudinary: Not configured (uploads will be disabled)")
    
    # Initialize Google Sheets service
    logger.info("🔍 Initializing Google Sheets service...")
    sheets_init = await google_sheets_service.initialize()
    if sheets_init:
        logger.info("✅ Google Sheets: Initialized successfully")
        # Test health
        health = await google_sheets_service.health_check()
        if health.get("status") == "healthy":
            logger.info("✅ Google Sheets: Health check passed")
        else:
            logger.warning(f"⚠️ Google Sheets: Health check failed - {health.get('error', 'Unknown error')}")
    else:
        logger.warning("⚠️ Google Sheets: Initialization failed (logging will be disabled)")
    
    # Create cache directory if needed
    if settings.cache_enabled:
        cache_dir = Path(settings.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Cache directory: {cache_dir}")
    
    # Create screenshots directory
    screenshots_dir = Path("./screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Screenshots directory: {screenshots_dir}")
    
    logger.info("🎯 All services initialized. Ready to start application!")
    return True


async def main():
    """Main startup function."""
    try:
        await initialize_services()
        logger.info("✅ Startup completed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
