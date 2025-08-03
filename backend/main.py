"""
Website Design Scorer Backend
Main application entry point.
"""
import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.app.core.settings import settings
from src.app.api.health import router as health_router
from src.app.api.master_analysis import router as master_analysis_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        print(f"Starting {settings.app_name} v{settings.app_version}")
        print(f"Environment: {settings.environment}")
        print(f"Debug mode: {settings.debug}")
        
        # Import startup initialization
        from startup import initialize_services
        
        # Initialize all services
        await initialize_services()
        
        # Create cache directory if it doesn't exist
        if settings.cache_enabled and not os.path.exists(settings.cache_dir):
            os.makedirs(settings.cache_dir, exist_ok=True)
            print(f"Created cache directory: {settings.cache_dir}")
            
    except Exception as e:
        print(f"Startup error: {e}")
        raise
    
    yield  # Application runs here
    



def create_app() -> FastAPI:
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered website design analysis and scoring system",
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(master_analysis_router)
    
    return app


app = create_app()


def main():
    """Run the application."""
    try:
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.debug,
            log_level="debug" if settings.debug else "info"
        )
    except Exception as e:
        print(f"Failed to start application: {e}")
        raise


if __name__ == "__main__":
    main()
