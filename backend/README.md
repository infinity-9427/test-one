# Website Design Scorer Backend

AI-powered website design analysis and scoring system with vision-based AI analysis.

## 🚀 Features

- **AI Vision Analysis**: Advanced visual design analysis using Ollama Qwen2.5VL model (always enabled)
- **Rule-based Scoring**: 5-category analysis (Typography, Color, Layout, Responsiveness, Accessibility)
- **Multi-Device Screenshots**: Desktop (1200x800) and mobile (375x667) capture
- **Cloud Integration**: Cloudinary storage with automatic optimization (always enabled)
- **Data Logging**: Google Sheets integration for analysis history
- **Unified API**: Single endpoint for complete analysis workflow

## 🎯 Primary API Endpoint

**All you need is one endpoint:**

```bash
POST /api/v1/master/analyze-complete
```

Complete website analysis in a single API call with screenshots, AI insights, scoring, and cloud storage.
**AI analysis and cloud storage are always enabled** for comprehensive results.

## 🚀 Quick Start

```bash
# Start all services
docker compose up -d

# Test the API - Simple request format
curl -X POST "http://localhost:8000/api/v1/master/analyze-complete" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}' | jq .
```

## 📚 Documentation

- **📖 [Complete API Documentation](./API_DOCUMENTATION.md)** - Full endpoint details and examples
- **🎯 [Service Overview](./SERVICE_OVERVIEW.md)** - Simplified API structure and usage guide
- **🔧 Interactive Docs:** http://localhost:8000/docs (when debug=true)

## 🔧 API Endpoints

### **Primary Endpoint**
- `POST /api/v1/master/analyze-complete` - **⭐ Complete website analysis**

### **Health Monitoring**  
- `GET /api/v1/health/simple` - Simple health check
- `GET /api/v1/health` - Detailed system health
- `GET /api/v1/master/health` - Service status

## Environment Variables

Configure in `.env`:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Development

1. Install dependencies: `uv pip install -e .`
2. Start Ollama: `docker run -d -p 11434:11434 ollama/ollama`
3. Pull Llama3: `docker exec -it <container> ollama pull llama3`
4. Run backend: `python main.py`

## Phase 3 Implementation

✅ **Rule-based Pre-checks**
- Typography analysis (font size, line height, hierarchy)
- Color harmony and contrast validation
- Layout and whitespace assessment
- Responsiveness indicators
- Accessibility compliance

✅ **Ollama LLM Integration**
- Llama3 model for design analysis
- Optimized prompts with custom rules
- Error handling and fallback strategies

✅ **API Integration**
- Async analysis processing
- Status polling and result retrieval
- Health monitoring for all services
