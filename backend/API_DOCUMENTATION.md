# Website Design Scorer API Documentation

## Overview

The Website Design Scorer is an AI-powered web service that provides comprehensive design analysis and scoring for websites. It combines rule-based analysis with AI vision analysis to evaluate typography, color schemes, layout, responsiveness, and accessibility.

## Features

### 🚀 Core Features
- **AI-Powered Analysis**: Uses Ollama with Qwen2.5VL vision model for visual design analysis
- **Multi-Device Screenshots**: Captures desktop (1200x800) and mobile (375x667) screenshots
- **Rule-Based Scoring**: Comprehensive analysis across 5 design categories
- **Cloud Storage**: Automatic screenshot upload to Cloudinary with optimization
- **Data Logging**: Optional Google Sheets integration for analysis history
- **Caching**: Smart caching system to avoid redundant operations

### 📊 Analysis Categories
1. **Typography** (25% weight): Font hierarchy, readability, contrast
2. **Color** (20% weight): Palette harmony, contrast ratios
3. **Layout** (25% weight): Whitespace, visual balance, structure
4. **Responsiveness** (15% weight): Mobile compatibility, viewport handling
5. **Accessibility** (15% weight): ARIA compliance, semantic HTML, alt text

### 🎯 Scoring System
- **Score Range**: 0-100 points
- **Grades**: A (90+), B (80-89), C (70-79), D (60-69), F (<60)
- **Categories**: Excellent (90+), Good (70-89), Fair (50-69), Poor (<50)

## API Endpoints

### Base URL
```
http://localhost:8000
```

## 1. Master Analysis API

### POST `/api/v1/master/analyze-complete`

**Description**: Complete website analysis workflow in a single endpoint. This is the primary endpoint that orchestrates screenshots, AI analysis, cloud uploads, and optional data logging.

**Request Body**:
```json
{
  "url": "https://example.com",
  "auto_log_to_sheets": true,
  "include_mobile": true,
  "include_ai_analysis": true,
  "store_cloudinary": true
}
```

**Parameters**:
- `url` (required): Website URL to analyze
- `auto_log_to_sheets` (optional, default: true): Log results to Google Sheets
- `include_mobile` (optional, default: true): Capture mobile screenshot
- `include_ai_analysis` (optional, default: true): Include AI vision analysis
- `store_cloudinary` (optional, default: true): Upload screenshots to cloud storage

**Response**:
```json
{
  "analysis_id": "master_1754222429",
  "url": "https://example.com",
  "status": "completed",
  "completed_at": "2025-08-03T12:00:00.000000",
  "analysis_duration": 25.5,
  "screenshots": [
    {
      "device": "desktop",
      "url": "https://example.com",
      "local_path": "/app/cache/screenshot_20250803_120000_1200x800.png",
      "cloudinary_url": "https://res.cloudinary.com/demo/image/upload/v1754222429/web-analyze-engine/website-screenshots/20250803_120000_desktop.webp",
      "captured_at": "2025-08-03T12:00:00.000000"
    },
    {
      "device": "mobile",
      "url": "https://example.com",
      "local_path": "/app/cache/screenshot_20250803_120000_375x667.png",
      "cloudinary_url": "https://res.cloudinary.com/demo/image/upload/v1754222429/web-analyze-engine/website-screenshots/20250803_120000_mobile.webp",
      "captured_at": "2025-08-03T12:00:00.000000"
    }
  ],
  "ai_insights": {
    "analysis_id": "analysis_1754222429",
    "url": "https://example.com",
    "analyzed_at": "2025-08-03T12:00:00.000000",
    "analysis_duration": 23.8,
    "status": "completed",
    "overall_score": 87.5,
    "score_category": "good",
    "score_grade": "B",
    "scores_breakdown": {
      "typography": 92,
      "color": 85,
      "layout": 88,
      "responsiveness": 95,
      "accessibility": 78
    },
    "report_summary": {
      "website_title": "Example Website",
      "evaluation_date": "August 03, 2025",
      "evaluation_time": "12:00 PM",
      "total_issues_found": 5,
      "critical_issues": [
        "ARIA accessibility violations detected"
      ],
      "strengths": [
        "Excellent typography and readability",
        "Good color scheme and harmony",
        "Well-structured layout and spacing",
        "Mobile-friendly design"
      ],
      "improvement_areas": [
        "Accessibility compliance"
      ]
    },
    "detailed_analysis": {
      "typography": {
        "score": 92,
        "grade": "A",
        "summary": "Excellent typography with clear hierarchy and readability",
        "issues": [],
        "recommendations": [
          "Typography is well-implemented"
        ]
      },
      "color": {
        "score": 85,
        "grade": "B",
        "summary": "Good color usage with room for minor improvements",
        "issues": [
          "Some color contrast issues detected"
        ],
        "recommendations": [
          "Improve color contrast for accessibility compliance"
        ]
      },
      "layout": {
        "score": 88,
        "grade": "B",
        "summary": "Good layout structure with some areas for refinement",
        "issues": [
          "Visual elements appear unbalanced"
        ],
        "recommendations": [
          "Improve grid alignment for more professional appearance"
        ]
      },
      "responsiveness": {
        "score": 95,
        "grade": "A",
        "summary": "Excellent mobile responsiveness and cross-device compatibility",
        "issues": [],
        "recommendations": [
          "Responsive design is well-implemented"
        ]
      },
      "accessibility": {
        "score": 78,
        "grade": "C",
        "summary": "Good accessibility with some areas for improvement",
        "issues": [
          "3 images missing alt text",
          "5 ARIA violations"
        ],
        "recommendations": [
          "Add descriptive alt text to all images",
          "Fix ARIA violations for screen reader compatibility"
        ]
      }
    },
    "rule_based_metrics": {
      "typography": {
        "base_font_size": 16,
        "line_height_ratio": 1.4,
        "contrast_violations": [],
        "font_fallbacks": ["Arial", "sans-serif"],
        "heading_hierarchy": [
          {
            "level": 1,
            "text": "Welcome to Example",
            "position": 0
          }
        ],
        "paragraph_lengths": [120, 85, 200],
        "score": 92
      },
      "color": {
        "primary_palette": [
          {
            "rgb": [51, 122, 183],
            "hex": "#337ab7"
          },
          {
            "rgb": [255, 255, 255],
            "hex": "#ffffff"
          }
        ],
        "harmony_violations": [],
        "saturation_violations": [],
        "contrast_violations": ["Low contrast detected"],
        "color_count": 6,
        "score": 85
      },
      "layout": {
        "whitespace_ratio": 0.45,
        "grid_violations": [],
        "section_padding": [],
        "visual_balance": {
          "x": 0,
          "y": 0,
          "balanced": false
        },
        "score": 88
      },
      "responsiveness": {
        "viewport_meta": true,
        "breakpoint_violations": [],
        "touch_target_violations": [],
        "image_scaling_issues": [],
        "score": 95
      },
      "accessibility": {
        "missing_alt_text": ["image1.jpg", "image2.png"],
        "aria_violations": [
          "Button without label",
          "Button without label"
        ],
        "semantic_html_issues": [
          "Missing main tag"
        ],
        "focus_order_issues": [],
        "score": 78
      }
    },
    "llm_analysis": {
      "content": "**SCREENSHOT VERIFICATION**: I can confirm this is the Example website. The visual layout shows a modern design with clear navigation and well-structured content sections...",
      "error": null,
      "model_used": "qwen2.5vl:latest",
      "vision_analysis": true
    },
    "screenshots": {
      "desktop": {
        "url": "https://example.com",
        "viewport_type": "desktop",
        "viewport": {
          "width": 1200,
          "height": 800
        },
        "local_path": "/app/cache/screenshot_20250803_120000_1200x800.png",
        "page_metrics": {
          "title": "Example Website",
          "url": "https://example.com",
          "viewport": {
            "width": 1200,
            "height": 800
          },
          "screenshot_size": 156789,
          "timestamp": "2025-08-03T12:00:00.000000"
        },
        "from_cache": false,
        "captured_at": "2025-08-03T12:00:00.000000"
      },
      "mobile": {
        "url": "https://example.com",
        "viewport_type": "mobile",
        "viewport": {
          "width": 375,
          "height": 667
        },
        "local_path": "/app/cache/screenshot_20250803_120000_375x667.png",
        "page_metrics": {
          "title": "Example Website",
          "url": "https://example.com",
          "viewport": {
            "width": 375,
            "height": 667
          },
          "screenshot_size": 89123,
          "timestamp": "2025-08-03T12:00:00.000000"
        },
        "from_cache": false,
        "captured_at": "2025-08-03T12:00:00.000000"
      }
    },
    "weights_applied": {
      "typography": 0.25,
      "color": 0.2,
      "layout": 0.25,
      "responsiveness": 0.15,
      "accessibility": 0.15
    },
    "rules_version": "1.0",
    "thresholds": {
      "excellent": 90,
      "good": 70,
      "fair": 50,
      "poor": 0
    }
  },
  "overall_score": 87.5,
  "scores_breakdown": {
    "typography": 92.0,
    "color": 85.0,
    "layout": 88.0,
    "responsiveness": 95.0,
    "accessibility": 78.0
  },
  "uploads": {
    "desktop_url": "https://res.cloudinary.com/demo/image/upload/v1754222429/web-analyze-engine/website-screenshots/20250803_120000_desktop.webp",
    "desktop_thumbnail": "https://res.cloudinary.com/demo/image/upload/c_fill,f_auto,h_200,q_auto,w_300/v1/web-analyze-engine/website-screenshots/20250803_120000_desktop",
    "mobile_url": "https://res.cloudinary.com/demo/image/upload/v1754222429/web-analyze-engine/website-screenshots/20250803_120000_mobile.webp",
    "mobile_thumbnail": "https://res.cloudinary.com/demo/image/upload/c_fill,f_auto,h_200,q_auto,w_300/v1/web-analyze-engine/website-screenshots/20250803_120000_mobile"
  },
  "sheet_entry_id": "sheets_1754222429",
  "errors": {}
}
```

### GET `/api/v1/master/health`

**Description**: Check the health status of all integrated services.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T12:00:00.000000",
  "services": {
    "screenshots": "available",
    "ai_analysis": "available", 
    "cloudinary": "available",
    "google_sheets": "available"
  },
  "details": {
    "ollama_model": "qwen2.5vl:latest",
    "cache_enabled": true,
    "environment": "development"
  }
}
```

## 2. System Health API

### GET `/api/v1/health`

**Description**: Comprehensive system health check including all services and dependencies.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T12:00:00.000000",
  "uptime": 3600.5,
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "ollama": {
      "status": "healthy",
      "model": "qwen2.5vl:latest",
      "response_time": 0.05
    },
    "cloudinary": {
      "status": "healthy",
      "upload_folder": "web-analyze-engine",
      "response_time": 0.12
    },
    "google_sheets": {
      "status": "healthy",
      "spreadsheet_id": "1vpj5Irkit2KyHoCjy5pEmsTjPQ3OwBvt5yH-nYfQvAk",
      "response_time": 0.08
    },
    "screenshot_service": {
      "status": "healthy",
      "browser": "chromium",
      "response_time": 0.03
    }
  },
  "system": {
    "cache_enabled": true,
    "cache_size": "150MB",
    "debug_mode": true
  }
}
```

### GET `/api/v1/health/simple`

**Description**: Simple health check endpoint for load balancers.

**Response**:
```json
{
  "status": "ok",
  "timestamp": "2025-08-03T12:00:00.000000"
}
```

## Usage Examples

### 1. Basic Website Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/microsoft/vscode",
    "store_cloudinary": true,
    "auto_log_to_sheets": true,
    "include_mobile": true,
    "include_ai_analysis": true
  }' | jq .
```

### 2. Quick Analysis Without Cloud Storage

```bash
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "store_cloudinary": false,
    "auto_log_to_sheets": false,
    "include_mobile": false
  }' | jq .
```

### 3. Mobile-Only Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://mobile-site.com",
    "include_mobile": true,
    "store_cloudinary": true
  }' | jq .
```

### 4. Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health" | jq .
```

### 5. Service Status Check

```bash
curl -X GET "http://localhost:8000/api/v1/master/health" | jq .
```

## Error Handling

### Common Error Responses

**400 Bad Request**:
```json
{
  "detail": "Invalid URL format provided"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "We're experiencing technical difficulties with our analysis service. Please try again later."
}
```

**Service Unavailable**:
```json
{
  "analysis_id": "master_1754222429",
  "status": "completed",
  "errors": {
    "ai_analysis": "AI vision analysis service is currently unavailable",
    "cloudinary_upload": "Cloud storage service temporarily unavailable"
  }
}
```

## Rate Limiting

- **Analysis Endpoint**: 10 requests per minute per IP
- **Health Endpoints**: 60 requests per minute per IP

## Authentication

Currently, the API does not require authentication. In production environments, implement:
- API key authentication
- JWT tokens for user sessions
- Rate limiting by user/API key

## SDKs and Integration

### JavaScript/Node.js Example

```javascript
const analyzeWebsite = async (url) => {
  const response = await fetch('http://localhost:8000/api/v1/master/analyze-complete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      store_cloudinary: true,
      auto_log_to_sheets: true,
      include_mobile: true,
      include_ai_analysis: true
    })
  });
  
  const result = await response.json();
  return result;
};

// Usage
analyzeWebsite('https://example.com')
  .then(result => {
    console.log(`Analysis completed with score: ${result.overall_score}`);
    console.log(`Desktop screenshot: ${result.uploads.desktop_url}`);
  })
  .catch(error => console.error('Analysis failed:', error));
```

### Python Example

```python
import requests
import json

def analyze_website(url):
    payload = {
        "url": url,
        "store_cloudinary": True,
        "auto_log_to_sheets": True,
        "include_mobile": True,
        "include_ai_analysis": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/master/analyze-complete",
        json=payload
    )
    
    return response.json()

# Usage
result = analyze_website("https://example.com")
print(f"Analysis completed with score: {result['overall_score']}")
print(f"Desktop screenshot: {result['uploads']['desktop_url']}")
```

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+ (for frontend)

### Environment Variables
```bash
# Required
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5vl:latest
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Optional
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials/google-sheets-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
CACHE_ENABLED=true
CACHE_TTL_HOURS=24
DEBUG=true
```

### Running the Service
```bash
# Start all services
docker compose up -d

# Check service status
curl http://localhost:8000/api/v1/health

# View logs
docker compose logs -f backend
```

## Support

For issues, feature requests, or questions:
- Check the health endpoints for service status
- Review error messages in the response
- Ensure all required environment variables are set
- Verify Ollama model is downloaded and running

## Changelog

### v1.0.0
- Initial release with master analysis endpoint
- AI vision analysis with Qwen2.5VL
- Multi-device screenshot capture
- Cloudinary integration
- Google Sheets logging
- Comprehensive scoring system
