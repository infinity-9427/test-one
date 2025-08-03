"""
Google Sheets integration service for logging analysis results.
Handles service account authentication, batch writes, and thumbnail embedding.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

import gspread
from google.auth.exceptions import GoogleAuthError
from google.oauth2.service_account import Credentials

from ..core.settings import settings

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Google Sheets service for logging website analysis results."""
    
    def __init__(self):
        """Initialize Google Sheets service with service account credentials."""
        self._client = None
        self._worksheet = None
        self._credentials = None
        self._initialized = False
        
    async def initialize(self) -> bool:
        """
        Initialize the Google Sheets client with service account credentials.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if not settings.google_sheets_credentials_path:
                logger.warning("Google Sheets credentials path not configured")
                return False
                
            if not settings.google_sheets_spreadsheet_id:
                logger.warning("Google Sheets spreadsheet ID not configured")
                return False
            
            # Check if credentials file exists
            creds_path = Path(settings.google_sheets_credentials_path)
            if not creds_path.exists():
                logger.error(f"Google Sheets credentials file not found: {creds_path}")
                return False
            
            # Load service account credentials
            self._credentials = Credentials.from_service_account_file(
                str(creds_path),
                scopes=[
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
            )
            
            # Initialize gspread client
            self._client = gspread.authorize(self._credentials)
            
            # Open the spreadsheet
            spreadsheet = self._client.open_by_key(settings.google_sheets_spreadsheet_id)
            
            # Get or create the main worksheet
            try:
                self._worksheet = spreadsheet.worksheet("Website Analysis Results")
            except gspread.WorksheetNotFound:
                logger.info("Creating 'Website Analysis Results' worksheet")
                self._worksheet = spreadsheet.add_worksheet(
                    title="Website Analysis Results",
                    rows=1000,
                    cols=15
                )
                await self._setup_headers()
            
            self._initialized = True
            logger.info("Google Sheets service initialized successfully")
            return True
            
        except GoogleAuthError as e:
            logger.error(f"Google Sheets authentication error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            return False
    
    async def _setup_headers(self):
        """Set up the header row for the worksheet."""
        try:
            headers = [
                "Timestamp",
                "Analysis ID",
                "URL",
                "Analyzed At",
                "Overall Score",
                "Typography Score",
                "Color Score", 
                "Layout Score",
                "Responsiveness Score",
                "Accessibility Score",
                "Desktop Screenshot",
                "Mobile Screenshot",
                "Desktop Thumbnail",
                "Mobile Thumbnail",
                "Analysis Duration (s)",
                "AI Summary"
            ]
            
            self._worksheet.append_row(headers)
            
            # Format header row
            self._worksheet.format('A1:P1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            logger.info("Google Sheets headers set up successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup Google Sheets headers: {e}")
            raise
    
    async def log_analysis_result(self, analysis_result: Dict[str, Any]) -> bool:
        """
        Log a single analysis result to Google Sheets.
        
        Args:
            analysis_result: The complete analysis result dictionary
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        try:
            if not self._initialized:
                logger.info("Google Sheets service not initialized, attempting to initialize...")
                init_success = await self.initialize()
                if not init_success:
                    logger.error("Failed to initialize Google Sheets service")
                    return False
            
            if not self._worksheet:
                logger.error("Google Sheets worksheet not available")
                return False
            
            # Extract data from analysis result
            analysis_id = analysis_result.get("analysis_id", "")
            url = analysis_result.get("url", "")
            analyzed_at = analysis_result.get("analyzed_at", "")
            overall_score = analysis_result.get("overall_score", 0)
            analysis_duration = analysis_result.get("analysis_duration", 0)
            
            # Extract score breakdown
            scores = analysis_result.get("scores_breakdown", {})
            typography_score = scores.get("typography", 0)
            color_score = scores.get("color", 0)
            layout_score = scores.get("layout", 0)
            responsiveness_score = scores.get("responsiveness", 0)
            accessibility_score = scores.get("accessibility", 0)
            
            # Extract screenshot URLs
            screenshots = analysis_result.get("screenshots", {})
            desktop_url = screenshots.get("desktop", {}).get("cloudinary_url", "")
            mobile_url = screenshots.get("mobile", {}).get("cloudinary_url", "")
            
            # Use direct image URLs instead of =IMAGE() formulas (more reliable)
            desktop_thumbnail = desktop_url if desktop_url else ""
            mobile_thumbnail = mobile_url if mobile_url else ""
            
            # Extract AI analysis summary
            llm_analysis = analysis_result.get("llm_analysis", {})
            ai_summary = llm_analysis.get("content", "")[:500] + "..." if len(llm_analysis.get("content", "")) > 500 else llm_analysis.get("content", "")
            
            # Prepare row data
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [
                current_timestamp,
                analysis_id,
                url,
                analyzed_at,
                round(overall_score, 2),
                round(typography_score, 2),
                round(color_score, 2),
                round(layout_score, 2),
                round(responsiveness_score, 2),
                round(accessibility_score, 2),
                desktop_url,
                mobile_url,
                desktop_thumbnail,
                mobile_thumbnail,
                round(analysis_duration, 2),
                ai_summary
            ]
            
            # Append to sheet
            self._worksheet.append_row(row_data)
            
            logger.info(f"Successfully logged analysis {analysis_id} to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to log analysis result to Google Sheets: {e}")
            return False
    
    async def log_batch_results(self, analysis_results: List[Dict[str, Any]]) -> int:
        """
        Log multiple analysis results to Google Sheets in batch.
        
        Args:
            analysis_results: List of analysis result dictionaries
            
        Returns:
            int: Number of results successfully logged
        """
        try:
            if not self._initialized:
                logger.info("Google Sheets service not initialized, attempting to initialize...")
                init_success = await self.initialize()
                if not init_success:
                    logger.error("Failed to initialize Google Sheets service")
                    return 0
            
            if not analysis_results:
                return 0
                
            if not self._worksheet:
                logger.error("Google Sheets worksheet not available")
                return 0
            
            # Prepare batch data
            batch_data = []
            for result in analysis_results:
                # Extract data (same logic as single result)
                analysis_id = result.get("analysis_id", "")
                url = result.get("url", "")
                analyzed_at = result.get("analyzed_at", "")
                overall_score = result.get("overall_score", 0)
                analysis_duration = result.get("analysis_duration", 0)
                
                scores = result.get("scores_breakdown", {})
                typography_score = scores.get("typography", 0)
                color_score = scores.get("color", 0)
                layout_score = scores.get("layout", 0)
                responsiveness_score = scores.get("responsiveness", 0)
                accessibility_score = scores.get("accessibility", 0)
                
                screenshots = result.get("screenshots", {})
                desktop_url = screenshots.get("desktop", {}).get("cloudinary_url", "")
                mobile_url = screenshots.get("mobile", {}).get("cloudinary_url", "")
                
                desktop_thumbnail = f'=IMAGE("{desktop_url}")' if desktop_url else ""
                mobile_thumbnail = f'=IMAGE("{mobile_url}")' if mobile_url else ""
                
                llm_analysis = result.get("llm_analysis", {})
                ai_summary = llm_analysis.get("content", "")[:500] + "..." if len(llm_analysis.get("content", "")) > 500 else llm_analysis.get("content", "")
                
                row_data = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    analysis_id,
                    url,
                    analyzed_at,
                    round(overall_score, 2),
                    round(typography_score, 2),
                    round(color_score, 2),
                    round(layout_score, 2),
                    round(responsiveness_score, 2),
                    round(accessibility_score, 2),
                    desktop_url,
                    mobile_url,
                    desktop_thumbnail,
                    mobile_thumbnail,
                    round(analysis_duration, 2),
                    ai_summary
                ]
                
                batch_data.append(row_data)
            
            # Append batch to sheet
            self._worksheet.append_rows(batch_data)
            
            logger.info(f"Successfully logged {len(batch_data)} analysis results to Google Sheets")
            return len(batch_data)
            
        except Exception as e:
            logger.error(f"Failed to log batch results to Google Sheets: {e}")
            return 0
    
    async def get_analysis_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve analysis history from Google Sheets.
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            List of analysis records
        """
        try:
            if not self._initialized:
                logger.info("Google Sheets service not initialized, attempting to initialize...")
                init_success = await self.initialize()
                if not init_success:
                    logger.error("Failed to initialize Google Sheets service")
                    return []
            
            if not self._worksheet:
                logger.error("Google Sheets worksheet not available")
                return []
            
            # Get all records (excluding header)
            records = self._worksheet.get_all_records()
            
            # Limit results and return most recent first
            recent_records = records[-limit:] if len(records) > limit else records
            recent_records.reverse()
            
            logger.info(f"Retrieved {len(recent_records)} analysis records from Google Sheets")
            return recent_records
            
        except Exception as e:
            logger.error(f"Failed to retrieve analysis history from Google Sheets: {e}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on Google Sheets service.
        
        Returns:
            Health check result with status and details
        """
        try:
            if not self._initialized:
                return {
                    "status": "unhealthy",
                    "error": "Service not initialized",
                    "details": {
                        "credentials_configured": bool(settings.google_sheets_credentials_path),
                        "spreadsheet_id_configured": bool(settings.google_sheets_spreadsheet_id)
                    }
                }
            
            # Try to access the worksheet
            if self._worksheet:
                worksheet_info = {
                    "title": self._worksheet.title,
                    "row_count": self._worksheet.row_count,
                    "col_count": self._worksheet.col_count
                }
            else:
                worksheet_info = {"error": "Worksheet not available"}
            
            return {
                "status": "healthy",
                "error": None,
                "details": {
                    "spreadsheet_id": settings.google_sheets_spreadsheet_id,
                    "worksheet": worksheet_info,
                    "credentials_valid": True
                }
            }
            
        except Exception as e:
            return {
                "status": "unhealthy", 
                "error": str(e),
                "details": {
                    "credentials_configured": bool(settings.google_sheets_credentials_path),
                    "spreadsheet_id_configured": bool(settings.google_sheets_spreadsheet_id)
                }
            }


# Global service instance
google_sheets_service = GoogleSheetsService()
