#!/usr/bin/env python3
"""
Test script for Website Design Scorer Backend.
Tests all services and workflows to ensure everything is working properly.
"""
import asyncio
import sys
import json
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from src.app.core.settings import settings
from src.app.services.screenshot_storage import screenshot_storage_service
from src.app.services.cloudinary import cloudinary_service
from src.app.services.google_sheets import google_sheets_service


async def test_screenshot_service():
    """Test screenshot capture service."""
    print("\n📸 Testing Screenshot Service...")
    try:
        # Test with a simple website
        test_url = "https://example.com"
        print(f"Capturing screenshot of: {test_url}")
        
        result = await screenshot_storage_service.capture_and_store(
            url=test_url,
            viewport_type="desktop",
            upload_to_cloud=False  # Start without cloud upload
        )
        
        print(f"✅ Screenshot captured successfully")
        print(f"   - Local path: {result['screenshot_data'].get('local_path', 'N/A')}")
        print(f"   - Page title: {result['screenshot_data'].get('page_metrics', {}).get('title', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Screenshot service failed: {e}")
        return False


async def test_cloudinary_service():
    """Test Cloudinary upload service."""
    print("\n☁️ Testing Cloudinary Service...")
    try:
        if not cloudinary_service.is_configured():
            print("⚠️ Cloudinary not configured - skipping test")
            return False
        
        # Test connection
        connection_ok = await cloudinary_service.test_connection()
        if connection_ok:
            print("✅ Cloudinary connection successful")
            return True
        else:
            print("❌ Cloudinary connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Cloudinary service failed: {e}")
        return False


async def test_google_sheets_service():
    """Test Google Sheets logging service."""
    print("\n📊 Testing Google Sheets Service...")
    try:
        # Initialize service
        init_success = await google_sheets_service.initialize()
        if not init_success:
            print("❌ Google Sheets initialization failed")
            return False
        
        print("✅ Google Sheets initialized successfully")
        
        # Test health check
        health = await google_sheets_service.health_check()
        print(f"Health status: {health.get('status', 'unknown')}")
        
        if health.get("status") == "healthy":
            print("✅ Google Sheets service is healthy")
            return True
        else:
            print(f"⚠️ Google Sheets service issues: {health.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Google Sheets service failed: {e}")
        return False


async def test_full_workflow():
    """Test the complete analysis workflow."""
    print("\n🔄 Testing Full Workflow...")
    try:
        # Test with example.com (reliable test site)
        test_url = "https://example.com"
        print(f"Running full analysis for: {test_url}")
        
        # Capture screenshot with cloud upload (if configured)
        result = await screenshot_storage_service.capture_and_store_both_viewports(
            url=test_url,
            upload_to_cloud=cloudinary_service.is_configured()
        )
        
        print("✅ Screenshot capture completed")
        print(f"   - Desktop captured: {'desktop' in result}")
        print(f"   - Mobile captured: {'mobile' in result}")
        
        # If we have screenshots and Google Sheets is configured, test logging
        if google_sheets_service._initialized:
            print("Testing Google Sheets logging...")
            
            # Create a test analysis result
            test_analysis = {
                "analysis_id": f"test_{int(asyncio.get_event_loop().time())}",
                "url": test_url,
                "analyzed_at": "2025-08-03T12:00:00Z",
                "overall_score": 85.5,
                "scores_breakdown": {
                    "typography": 90,
                    "color": 80,
                    "layout": 85,
                    "responsiveness": 88,
                    "accessibility": 82
                },
                "screenshots": {
                    "desktop": result.get("desktop", {}).get("storage_data", {}) if result.get("desktop") else {},
                    "mobile": result.get("mobile", {}).get("storage_data", {}) if result.get("mobile") else {}
                },
                "llm_analysis": {
                    "content": "Test analysis summary from automated testing"
                },
                "analysis_duration": 12.5
            }
            
            # Log to sheets
            log_success = await google_sheets_service.log_analysis_result(test_analysis)
            if log_success:
                print("✅ Google Sheets logging successful")
            else:
                print("⚠️ Google Sheets logging failed")
        
        print("✅ Full workflow test completed")
        return True
        
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("🧪 Website Design Scorer - Test Suite")
    print("=" * 50)
    
    # Test results
    results = {}
    
    # Test individual services
    results["screenshot"] = await test_screenshot_service()
    results["cloudinary"] = await test_cloudinary_service()
    results["google_sheets"] = await test_google_sheets_service()
    
    # Test full workflow
    results["full_workflow"] = await test_full_workflow()
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 30)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{service:15} {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Your setup is working correctly.")
        return True
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
