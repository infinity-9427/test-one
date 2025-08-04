# 🎯 Website Design Scoring & Reporting Tool

![App Screenshot Desktop](/img-1.webp)
*Desktop screenshot capture and analysis interface*

![App Screenshot Mobile](/img-2.webp)
*Mobile-responsive design analysis view*

A comprehensive **automated website design analysis system** that combines AI vision analysis with rule-based scoring to provide professional website design evaluations. The system captures multi-device screenshots, analyzes design quality across 5 key categories, stores results in cloud storage, and maintains analysis history in Google Sheets.

## 🚀 Features

### Core Capabilities
- 🤖 **AI Vision Analysis**: Advanced visual design analysis using Qwen2.5VL vision-language model
- 📏 **Rule-Based Scoring**: Comprehensive 5-category analysis (Typography, Color, Layout, Responsiveness, Accessibility)
- 📱 **Multi-Device Screenshots**: Automated capture for desktop (1200x800) and mobile (375x667) viewports
- ☁️ **Cloud Storage**: Cloudinary integration with automatic optimization and CDN distribution
- 📊 **Google Sheets Integration**: Automated logging of analysis results with timestamps and scores
- 🔄 **Single API Endpoint**: Complete analysis workflow in one API call

### Analysis Categories
| Category | Weight | Key Metrics |
|----------|--------|-------------|
| **Typography** | 20% | Font size ≥16px, line-height 1.4-1.6, contrast ratios, hierarchy |
| **Color Design** | 20% | Harmony checks, saturation limits, accessibility compliance |
| **Layout & Structure** | 20% | Grid alignment, whitespace ratio 30-50%, visual balance |
| **Responsiveness** | 20% | Viewport meta, breakpoints, touch targets ≥44px |
| **Accessibility** | 20% | Alt text, ARIA labels, semantic HTML, focus indicators |

## 🏗️ Architecture

### Backend Services
- **FastAPI**: RESTful API with async processing
- **Ollama + Qwen2.5VL**: Local AI model for vision analysis
- **Playwright**: Automated browser screenshots
- **Cloudinary**: Image storage and optimization
- **Google Sheets API**: Data persistence and reporting

### Frontend (Next.js)
- **React 19 + Next.js 15**: Modern React framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Radix UI**: Accessible component library

## 📋 Prerequisites

### Required Software
- **Docker & Docker Compose**: Container orchestration
- **Node.js 18+**: Frontend development (if running locally)
- **Python 3.11+**: Backend development (if running locally)

### Required API Keys & Credentials

#### 1. Cloudinary Account (Image Storage)
1. Sign up at [cloudinary.com](https://cloudinary.com)
2. Get your credentials from Dashboard → API Keys:
   - Cloud Name
   - API Key
   - API Secret

#### 2. Google Sheets API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
4. Create Service Account:
   - Navigate to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Download JSON credentials file
5. Create Google Spreadsheet:
   - Share with service account email (from JSON file)
   - Copy spreadsheet ID from URL

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd test-one
```

### 2. Configure Environment Variables

Create environment file in backend directory:
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` with your credentials:
```bash
# AI Model Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5vl:latest
OLLAMA_TIMEOUT=120

# Cloudinary Configuration (REQUIRED)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Google Sheets Configuration (REQUIRED)
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google-sheets-service-account.json

# Application Settings
ENVIRONMENT=development
DEBUG=true
CACHE_ENABLED=true
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000
```

### 3. Add Google Credentials

Place your Google service account JSON file:
```bash
# Copy your downloaded JSON file to:
backend/credentials/google-sheets-service-account.json
```

### 4. Start the Application

#### Option A: Automated Setup (Recommended)
```bash
# From project root
./start.sh
```

#### Option B: Manual Docker Setup
```bash
cd backend

# Build and start services
docker compose build
docker compose up -d

# Monitor startup logs
docker compose logs -f
```

### 5. Verify Installation

Check service health:
```bash
# API Health Check
curl http://localhost:8000/api/v1/health

# Ollama Model Status
curl http://localhost:11434/api/tags
```

Access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 API Usage

### Primary Endpoint

**Complete Website Analysis:**
```bash
POST /api/v1/master/analyze-complete
```

### Basic Usage Example

```bash
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://stripe.com",
    "auto_log_to_sheets": true,
    "include_mobile": true
  }' | jq .
```

### Advanced Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "auto_log_to_sheets": false,
    "include_mobile": false,
    "analysis_type": "quick"
  }' | jq .
```

### Response Structure

```json
{
  "analysis_id": "master_1722692431",
  "url": "https://stripe.com",
  "status": "completed",
  "completed_at": "2025-08-03T11:40:31.456789",
  "analysis_duration": 12.45,
  "overall_score": 67.2,
  "grade": "D",
  "scores_breakdown": {
    "typography": 72.0,
    "color": 68.0,
    "layout": 75.0,
    "responsiveness": 65.0,
    "accessibility": 56.0
  },
  "screenshots": [
    {
      "device": "desktop",
      "cloudinary_url": "https://res.cloudinary.com/.../desktop.webp",
      "thumbnail_url": "https://res.cloudinary.com/.../w_300,h_200",
      "captured_at": "2025-08-03T11:40:19.123456"
    },
    {
      "device": "mobile",
      "cloudinary_url": "https://res.cloudinary.com/.../mobile.webp",
      "thumbnail_url": "https://res.cloudinary.com/.../w_200,h_300",
      "captured_at": "2025-08-03T11:40:20.654321"
    }
  ],
  "ai_insights": {
    "design_observations": "Clean, professional layout with strong visual hierarchy...",
    "strengths": ["Clear navigation", "Consistent branding", "Good color contrast"],
    "improvement_suggestions": ["Increase mobile touch targets", "Add more whitespace"],
    "overall_assessment": "The website demonstrates professional design standards..."
  }
}
```

## 🛠️ Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

Access development frontend at: http://localhost:3000

### Environment Variables Reference

#### Backend Configuration
```bash
# Core API Settings
ENVIRONMENT=development|production
DEBUG=true|false
HOST=0.0.0.0
PORT=8000

# AI Model Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5vl:latest
OLLAMA_TIMEOUT=120

# Screenshot Settings
PLAYWRIGHT_HEADLESS=true|false
PLAYWRIGHT_TIMEOUT=30000
CACHE_ENABLED=true|false
CACHE_DIR=./cache

# Cloud Storage (Cloudinary)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
UPLOAD_FOLDER=./screenshots

# Google Sheets Integration
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google-sheets-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
```

## 📁 Project Structure

```
test-one/
├── README.md                    # This file
├── start.sh                     # Quick start script
├── img-1.webp                   # App screenshot (desktop)
├── img-2.webp                   # App screenshot (mobile)
│
├── backend/                     # Python FastAPI Backend
│   ├── src/app/
│   │   ├── api/
│   │   │   ├── master_analysis.py   # 🎯 Primary API endpoint
│   │   │   └── health.py            # Health monitoring
│   │   ├── services/
│   │   │   ├── ai_analysis.py       # AI vision analysis
│   │   │   ├── screenshot.py        # Playwright capture
│   │   │   ├── cloudinary.py        # Cloud storage
│   │   │   ├── google_sheets.py     # Data logging
│   │   │   └── prompts.py           # AI prompt templates
│   │   └── utils/
│   ├── credentials/             # 🔒 API keys (gitignored)
│   │   ├── google-sheets-service-account.json
│   │   └── README.md
│   ├── cache/                   # 🗂️ Temp screenshots (gitignored)
│   ├── docker-compose.yml       # Service orchestration
│   ├── Dockerfile              # Backend container
│   ├── pyproject.toml          # Python dependencies
│   ├── .env                    # Environment variables (create from .env.example)
│   └── start_backend.sh        # Backend startup script
│
└── frontend/                   # Next.js 15 Frontend
    ├── src/app/
    │   ├── page.tsx            # Main application
    │   ├── layout.tsx          # Root layout
    │   └── globals.css         # Global styles
    ├── src/components/
    │   ├── analysis-results.tsx    # Results display
    │   ├── screenshot-gallery.tsx # Image gallery
    │   ├── score-display.tsx      # Score visualization
    │   └── ui/                     # Radix UI components
    ├── public/
    │   ├── logo-web-engine.png # App logo
    │   └── manifest.json       # PWA manifest
    ├── package.json            # Node.js dependencies
    └── next.config.ts          # Next.js configuration
```

## 🔧 Troubleshooting

### Common Issues

#### 1. AI Model Download Issues
```bash
# Check model status
docker compose exec ollama ollama list

# Manual model download
docker compose exec ollama ollama pull qwen2.5vl:latest

# Check model size (should be ~5GB)
docker compose exec ollama ollama show qwen2.5vl:latest
```

#### 2. Google Sheets Authentication
```bash
# Verify credentials file exists
ls -la backend/credentials/

# Check service account email in JSON file
cat backend/credentials/google-sheets-service-account.json | jq .client_email

# Ensure spreadsheet is shared with service account
```

#### 3. Cloudinary Upload Issues
```bash
# Test Cloudinary credentials
curl -X POST \
  "https://api.cloudinary.com/v1_1/YOUR_CLOUD_NAME/image/upload" \
  -F "file=@test_image.jpg" \
  -F "upload_preset=YOUR_UPLOAD_PRESET"
```

#### 4. Screenshot Capture Problems
```bash
# Check Playwright browser installation
docker compose exec backend playwright install chromium

# Test basic screenshot
docker compose exec backend python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    page.screenshot(path='test.png')
    browser.close()
    print('Screenshot test successful')
"
```

### Service Health Monitoring

```bash
# Check all service status
docker compose ps

# View service logs
docker compose logs backend
docker compose logs ollama

# Monitor real-time logs
docker compose logs -f

# Restart specific service
docker compose restart backend
```

### Performance Optimization

#### 1. AI Analysis Speed
- Use `analysis_type: "quick"` for faster results
- Disable mobile screenshots if not needed: `include_mobile: false`
- Enable caching: `CACHE_ENABLED=true`

#### 2. Memory Usage
```bash
# Monitor container memory usage
docker stats

# Limit Ollama memory (in docker-compose.yml)
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 8G
```

## 📊 Example Analysis Results

### High-Scoring Website (Grade A: 90-100)
- **Apple.com**: 93.5/100
  - Typography: 95/100 (Perfect hierarchy, readable fonts)
  - Color: 92/100 (Consistent brand colors, high contrast)
  - Layout: 94/100 (Clean spacing, balanced composition)
  - Responsiveness: 96/100 (Excellent mobile experience)
  - Accessibility: 91/100 (Good semantic HTML, ARIA labels)

### Medium-Scoring Website (Grade C: 70-79)
- **Stripe.com**: 67.2/100
  - Typography: 72/100 (Good hierarchy, some contrast issues)
  - Color: 68/100 (Professional palette, limited accessibility)
  - Layout: 75/100 (Well-structured, could use more whitespace)
  - Responsiveness: 65/100 (Basic mobile support, touch targets small)
  - Accessibility: 56/100 (Missing alt text, limited ARIA support)

### Areas for Improvement
- **Touch Target Size**: Minimum 44px for mobile usability
- **Color Contrast**: WCAG AA compliance (4.5:1 ratio)
- **Typography Scale**: Consistent font size progression
- **Whitespace Ratio**: 30-50% of page area for better readability

## 🎯 API Endpoints Reference

### Health & Status
```bash
GET /api/v1/health                 # Detailed system health
GET /api/v1/health/simple         # Basic health check
GET /api/v1/master/health         # Service-specific status
```

### Analysis Endpoints
```bash
POST /api/v1/master/analyze-complete    # 🎯 Primary analysis endpoint
```

### Request Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | **required** | Website URL to analyze |
| `auto_log_to_sheets` | boolean | true | Log results to Google Sheets |
| `include_mobile` | boolean | true | Capture mobile screenshots |
| `analysis_type` | string | "pdf_report" | Analysis depth: "quick", "detailed", "pdf_report" |

## 🚀 Production Deployment

### Docker Production Setup
```bash
# Production environment
export ENVIRONMENT=production
export DEBUG=false

# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy with resource limits
docker compose -f docker-compose.prod.yml up -d
```

### Environment Security
```bash
# Secure credential management
chmod 600 backend/credentials/*.json
chown root:root backend/credentials/

# Use Docker secrets for sensitive data
docker secret create google_creds backend/credentials/google-sheets-service-account.json
```

### Monitoring & Scaling
- **Health Checks**: Automated monitoring with `/health` endpoints
- **Resource Limits**: Configure memory/CPU limits in docker-compose.yml
- **Load Balancing**: Deploy multiple backend instances
- **CDN Integration**: Cloudinary provides global CDN distribution

## 📄 License

This project is developed as a technical assessment demonstrating automated website design analysis capabilities using modern AI and cloud technologies.

---

## 🤝 Technical Assessment Context

This application was developed as a comprehensive solution for **automated website design scoring and reporting**. The system demonstrates:

- **Full-Stack Development**: FastAPI backend + Next.js frontend
- **AI Integration**: Vision-language models for design analysis
- **Cloud Services**: Cloudinary storage + Google Sheets integration
- **Containerization**: Docker orchestration with health monitoring
- **API Design**: RESTful endpoints with comprehensive documentation
- **Real-World Application**: Production-ready code with error handling

The tool provides objective, consistent website design evaluation suitable for design agencies, developers, and businesses looking to improve their web presence through data-driven insights.

**Key Achievement**: Single API call delivers complete analysis including screenshots, AI insights, scoring, cloud storage, and automated reporting - demonstrating end-to-end automation capabilities.

## 🚀 Features

### **Phase 3 - AI Analysis Engine (Current)**
- ✅ **Hybrid Scoring System**: Combines rule-based analysis with AI-powered insights
- ✅ **LLM Integration**: Uses Ollama + Llama3 for intelligent design evaluation
- ✅ **Real-time Analysis**: Live progress tracking and status updates
- ✅ **Custom Rules Engine**: Based on 20+ years of UI/UX expertise
- ✅ **Multi-viewport Screenshots**: Desktop (1200x800) and Mobile (375x667)
- ✅ **Cloud Storage**: Cloudinary integration for optimized image storage
- ✅ **Comprehensive Metrics**: Typography, Color, Layout, Responsiveness, Accessibility
- ✅ **RESTful API**: Complete CRUD operations for analysis management
- ✅ **Docker Orchestration**: Production-ready containerized deployment

### **Core Analysis Categories**
1. **📐 Typography & Readability** (25% weight)
   - Font size validation (≥16px)
   - Line height ratios (1.4-1.6)
   - WCAG contrast compliance
   - Heading hierarchy structure
   - Paragraph length optimization

2. **🎨 Color & Visual Hierarchy** (20% weight)
   - Color harmony analysis
   - Saturation moderation
   - UI control contrast
   - Color consistency checks

3. **📱 Layout & Responsiveness** (25% weight)
   - 8px grid adherence
   - Whitespace ratio analysis
   - Mobile-first design validation
   - Touch target sizing

4. **♿ Accessibility & Semantics** (15% weight)
   - Alt text validation
   - ARIA compliance
   - Semantic HTML structure
   - Keyboard navigation

5. **🧠 AI-Powered Insights** (15% weight)
   - LLM-generated recommendations
   - Design quality assessment
   - User experience evaluation

## 🛠 Tech Stack

### **Backend**
- **FastAPI** - High-performance API framework
- **Playwright** - Screenshot capture and browser automation
- **Ollama + Llama3** - Local LLM for AI analysis
- **BeautifulSoup** - HTML/CSS parsing and analysis
- **Cloudinary** - Image optimization and CDN
- **Docker** - Containerization and orchestration
- **uv** - Modern Python package management

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Modern component library

## 📦 Installation & Setup

### Prerequisites
- **Docker & Docker Compose** (required)
- **Git** (required)
- **Node.js 18+** (for frontend development)

### 1. Clone the Repository
```bash
git clone https://github.com/infinity-9427/test-one.git
cd test-one
```

### 2. Environment Configuration

#### Backend Environment Variables
Create `/backend/.env`:
```env
# Application Settings
ENVIRONMENT=local
DEBUG=true
APP_NAME="Website Design Scorer"
APP_VERSION="0.1.0"

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Ollama Settings (for AI Analysis)
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3
OLLAMA_TIMEOUT=60

# Cloudinary Settings (Required for image storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
UPLOAD_FOLDER=web-analyze-engine

# Cache Settings
CACHE_ENABLED=true
CACHE_TTL_HOURS=24
CACHE_DIR=/app/cache

# Playwright Settings
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000
```

#### Frontend Environment Variables
Create `/frontend/.env.local`:
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Website Design Scorer"
NEXT_PUBLIC_APP_VERSION="0.1.0"

# Analytics (Optional)
NEXT_PUBLIC_GA_ID=your_ga_id
```

### 3. Docker Setup & Installation

**Note: This project uses `pnpm` as the package manager for the frontend. Make sure you have pnpm installed globally:**

```bash
npm install -g pnpm
```

#### Backend Setup (Required)
```bash
# Navigate to backend directory
cd backend

# Build and start all services (Ollama + Backend + Llama3 model)
docker compose build
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

#### Frontend Setup (Development)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (pnpm is required)
pnpm install

# Start development server
pnpm dev
```

## 🚀 Running the Application

### 1. Start Backend Services
```bash
cd backend
docker compose up -d
```

**Services Started:**
- **Ollama**: LLM service on port `11434`
- **Backend API**: FastAPI server on port `8000`
- **Llama3 Model**: Auto-downloaded (4.7GB, takes 5-10 minutes)

### 2. Start Frontend (Optional)
```bash
cd frontend
pnpm dev
```
Access at: `http://localhost:3000`

### 3. Verify Installation
```bash
# Test API health
curl http://localhost:8000/api/v1/health

# Test screenshot capture
curl -X POST "http://localhost:8000/api/v1/screenshots/capture" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "format": "PNG"}'

# Run comprehensive test
cd backend
python test_analysis.py
```

## 📡 API Endpoints

### Health & Status
- `GET /api/v1/health` - System health check
- `GET /api/v1/analysis/health` - Analysis engine health

### Screenshot Capture
- `POST /api/v1/screenshots/capture` - Capture website screenshots
- `GET /api/v1/screenshots/list` - List captured screenshots

### Analysis Engine
- `POST /api/v1/analysis/analyze` - Start website analysis
- `GET /api/v1/analysis/status/{id}` - Check analysis progress
- `GET /api/v1/analysis/result/{id}` - Get analysis results
- `GET /api/v1/analysis/list` - List all analyses

### Example API Usage
```bash
# Start analysis
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com",
    "include_mobile": true,
    "include_llm_analysis": true
  }'

# Check status
curl http://localhost:8000/api/v1/analysis/status/analysis_123

# Get results
curl http://localhost:8000/api/v1/analysis/result/analysis_123
```

## 🔧 Development

### Backend Development
```bash
cd backend

# Install dependencies with uv
pip install uv
uv pip install -e .

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python test_analysis.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies (pnpm required)
pnpm install

# Start development
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

## 📊 Analysis Results Structure

```json
{
  "analysis_id": "analysis_1234567890",
  "status": "completed",
  "overall_score": 81.5,
  "analysis_duration": 48.69,
  "scores_breakdown": {
    "typography": 100.0,
    "color": 90.0,
    "layout": 70.0,
    "responsiveness": 100.0,
    "accessibility": 40.0
  },
  "llm_analysis": {
    "content": "**Overall Design Quality Assessment:** 6/10\n\nThe website's design quality is average...",
    "processing_time": 45.2
  },
  "screenshots": {
    "desktop": {
      "local_path": "cache/screenshot_desktop.png",
      "cloudinary_url": "https://res.cloudinary.com/...",
      "viewport": {"width": 1200, "height": 800}
    },
    "mobile": {
      "local_path": "cache/screenshot_mobile.png", 
      "cloudinary_url": "https://res.cloudinary.com/...",
      "viewport": {"width": 375, "height": 667}
    }
  },
  "rule_analysis": {
    "typography": {
      "score": 100.0,
      "issues": [],
      "metrics": {
        "base_font_size": 16,
        "line_height_ratio": 1.5,
        "heading_hierarchy": [...],
        "font_fallbacks": [...]
      }
    }
  }
}
```

## 🐳 Docker Commands

### Basic Operations
```bash
# Build and start
docker compose up -d --build

# Stop services
docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f ollama

# Restart specific service
docker compose restart backend

# Check service health
docker compose ps
```

### Troubleshooting
```bash
# Rebuild without cache
docker compose build --no-cache

# Remove volumes and rebuild
docker compose down -v
docker compose up -d --build

# Access container shell
docker compose exec backend bash
docker compose exec ollama bash

# Check Ollama models
docker compose exec ollama ollama list
```

## 🔍 Monitoring & Debugging

### Service Health Checks
```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Ollama health  
curl http://localhost:11434/api/tags

# Full system test
cd backend && python test_analysis.py
```

### Log Monitoring
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f ollama-init

# Analysis progress
curl http://localhost:8000/api/v1/analysis/list
```


---

For issues and questions:
- 🐛 [Report Bug](https://github.com/infinity-9427/test-one/issues)
