# Website Design Scorer Backend

AI-powered website design analysis and scoring system using Ollama + Llama3.

## Features

- **Rule-based Analysis**: Typography, color harmony, layout, responsiveness, accessibility checks
- **AI-powered Insights**: LLM analysis using Llama3 via Ollama
- **Screenshot Capture**: Multi-viewport screenshots with Playwright
- **Cloud Storage**: Cloudinary integration for image management
- **REST API**: FastAPI-based endpoints with async processing

## Quick Start with Docker

```bash
# Start all services (Ollama + Llama3 + Backend)
./start.sh

# Test the API
python test_analysis.py
```

## API Endpoints

- `GET /api/v1/health` - Basic health check
- `GET /api/v1/analysis/health` - Analysis services health
- `POST /api/v1/analysis/analyze` - Start website analysis
- `GET /api/v1/analysis/status/{id}` - Check analysis status
- `GET /api/v1/analysis/result/{id}` - Get analysis results

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
