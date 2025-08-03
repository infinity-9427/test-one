"""
Health check endpoints and service connectivity verification.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
import asyncio
from datetime import datetime

from ..core.settings import settings


class HealthStatus(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    environment: str
    services: Dict[str, Dict[str, Any]]


class ServiceHealth(BaseModel):
    """Individual service health status."""
    status: str
    response_time_ms: float
    error: str | None = None


router = APIRouter(tags=["Health"])


async def check_ollama_health() -> ServiceHealth:
    """Check Ollama service connectivity."""
    try:
        start_time = datetime.now()
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        if response.status_code == 200:
            return ServiceHealth(
                status="healthy",
                response_time_ms=response_time
            )
        else:
            return ServiceHealth(
                status="unhealthy",
                response_time_ms=response_time,
                error=f"HTTP {response.status_code}"
            )
            
    except Exception as e:
        return ServiceHealth(
            status="unhealthy",
            response_time_ms=0,
            error=str(e)
        )


async def check_cloudinary_health() -> ServiceHealth:
    """Check Cloudinary service connectivity."""
    try:
        # Check if credentials are configured
        if not all([settings.cloudinary_cloud_name, settings.cloudinary_api_key, settings.cloudinary_api_secret]):
            return ServiceHealth(
                status="not_configured",
                response_time_ms=0,
                error=f"Cloudinary credentials not configured. cloud_name='{settings.cloudinary_cloud_name}', api_key='{settings.cloudinary_api_key[:10]}...', api_secret='{'*' * len(settings.cloudinary_api_secret) if settings.cloudinary_api_secret else 'None'}'"
            )
        
        # Actually test Cloudinary connectivity with a real API call
        import cloudinary
        import cloudinary.api
        from cloudinary.exceptions import Error as CloudinaryError
        
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
        )
        
        start_time = datetime.now()
        try:
            result = cloudinary.api.ping()
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ServiceHealth(
                status="healthy",
                response_time_ms=response_time,
                error=None
            )
        except CloudinaryError as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            return ServiceHealth(
                status="unhealthy",
                response_time_ms=response_time,
                error=f"Cloudinary API error: {str(e)} (code: {getattr(e, 'code', 'unknown')})"
            )
            
    except Exception as e:
        return ServiceHealth(
            status="unhealthy",
            response_time_ms=0,
            error=f"Unexpected error: {str(e)} (type: {type(e).__name__})"
        )


async def check_google_sheets_health() -> ServiceHealth:
    """Check Google Sheets service connectivity."""
    try:
        from ..services.google_sheets import google_sheets_service
        
        start_time = datetime.now()
        health_result = await google_sheets_service.health_check()
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return ServiceHealth(
            status=health_result["status"],
            response_time_ms=response_time,
            error=health_result.get("error")
        )
        
    except Exception as e:
        return ServiceHealth(
            status="unhealthy",
            response_time_ms=0,
            error=str(e)
        )


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Comprehensive health check endpoint.
    
    Returns application status and connectivity to external services.
    """
    try:
        # Run service checks concurrently
        results = await asyncio.gather(
            check_ollama_health(),
            check_cloudinary_health(),
            check_google_sheets_health(),
            return_exceptions=True
        )
        
        ollama_health, cloudinary_health, google_sheets_health = results
        
        # Handle any exceptions from the gather
        if isinstance(ollama_health, Exception):
            ollama_health = ServiceHealth(
                status="error",
                response_time_ms=0,
                error=str(ollama_health)
            )
            
        if isinstance(cloudinary_health, Exception):
            cloudinary_health = ServiceHealth(
                status="error", 
                response_time_ms=0,
                error=str(cloudinary_health)
            )
            
        if isinstance(google_sheets_health, Exception):
            google_sheets_health = ServiceHealth(
                status="error",
                response_time_ms=0,
                error=str(google_sheets_health)
            )
        
        services = {}
        
        # Process ollama health
        if isinstance(ollama_health, ServiceHealth):
            services["ollama"] = ollama_health.model_dump()
        else:
            services["ollama"] = ServiceHealth(
                status="error",
                response_time_ms=0,
                error=str(ollama_health)
            ).model_dump()
            
        # Process cloudinary health  
        if isinstance(cloudinary_health, ServiceHealth):
            services["cloudinary"] = cloudinary_health.model_dump()
        else:
            services["cloudinary"] = ServiceHealth(
                status="error",
                response_time_ms=0,
                error=str(cloudinary_health)
            ).model_dump()
            
        # Process google sheets health
        if isinstance(google_sheets_health, ServiceHealth):
            services["google_sheets"] = google_sheets_health.model_dump()
        else:
            services["google_sheets"] = ServiceHealth(
                status="error",
                response_time_ms=0,
                error=str(google_sheets_health)
            ).model_dump()
        
        # Determine overall status
        overall_status = "healthy"
        if any(service["status"] in ["unhealthy", "error"] for service in services.values()):
            overall_status = "degraded"
        elif any(service["status"] == "not_configured" for service in services.values()):
            overall_status = "partial"
            
        return HealthStatus(
            status=overall_status,
            timestamp=datetime.now(),
            version=settings.app_version,
            environment=settings.environment,
            services=services
        )
        
    except Exception as e:
        print(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="We're experiencing technical difficulties with the health check. Please try again later."
        )


@router.get("/health/simple")
async def simple_health_check():
    """Simple health check endpoint that just returns OK."""
    return {"status": "ok", "timestamp": datetime.now()}
