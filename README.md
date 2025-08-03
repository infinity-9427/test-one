# Website Design Scorer & Reporting Tool

*AI-Powered Website Design Analysis with Phase 3 Advanced Scoring Engine*

A comprehensive tool for analyzing and scoring website design quality using rule-based metrics and AI-powered insights. This project combines traditional design principles with modern AI technology to provide detailed, actionable feedback on website design.

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

# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
# or
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
npm run dev
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

# Install dependencies
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
