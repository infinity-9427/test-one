"""
Application settings configuration using Pydantic Settings.
Handles environment variable auto-loading and validation.
"""
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Literal
import os


class Settings(BaseSettings):
    """Application settings with environment variable auto-loading."""
    
    # Application settings
    app_name: str = Field(default="Website Design Scorer", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: Literal["local", "prod"] = Field(default="local", description="Environment")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    ollama_model: str = Field(default="phi4", description="Ollama model to use")
    ollama_timeout: int = Field(default=60, description="Ollama request timeout in seconds")
    
    # Cloudinary settings (will be set when API keys are provided)
    upload_folder: str = Field(default="", description="Upload folder name")
    cloudinary_cloud_name: str = Field(default="", description="Cloudinary cloud name")
    cloudinary_api_key: str = Field(default="", description="Cloudinary API key")
    cloudinary_api_secret: str = Field(default="", description="Cloudinary API secret")
    
    # Google Sheets settings (will be set when API keys are provided)
    google_sheets_credentials_path: str = Field(default="", description="Path to Google Sheets credentials JSON")
    google_sheets_spreadsheet_id: str = Field(default="", description="Google Sheets spreadsheet ID")
    
    # Playwright settings
    playwright_headless: bool = Field(default=True, description="Run Playwright in headless mode")
    playwright_timeout: int = Field(default=30000, description="Playwright timeout in milliseconds")
    
    # Cache settings
    cache_enabled: bool = Field(default=True, description="Enable screenshot caching")
    cache_ttl_hours: int = Field(default=24, description="Cache TTL in hours")
    cache_dir: str = Field(default="./cache", description="Cache directory path")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
settings = Settings()
