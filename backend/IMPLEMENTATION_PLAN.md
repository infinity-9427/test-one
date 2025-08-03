# Website Design Scorer Backend - Implementation Plan

## Overview
This backend will analyze website designs using Llama3 via Ollama, capture screenshots, store them in Cloudinary, and generate comprehensive design assessment reports.

CONSTRAINTS:  dont use fallback strategy, handle error propertly with try catch blocks, if require auth api key plz request me, i shall provide it tp you

## Technology Stack
- **FastAPI**: REST API framework
- **Pydantic**: Data validation and serialization
- **Docker**: Containerization
- **Ollama + Llama3**: AI-powered design analysis
- **Selenium/Playwright**: Web scraping and screenshot capture
- **Cloudinary**: Image storage and management
- **Google Sheets API**: Data logging
- **ReportLab/WeasyPrint**: PDF generation

## Implementation Phases

Phase 1: Core Infra

    Pydantic Settings: use Settings Management so env vars auto-load into your models.

    Health Check: extend beyond a simple “OK”—also check Ollama and Cloudinary connectivity.

    Local vs Prod Profiles: use .env.local + .env.prod for different defaults (e.g. headless vs headed).

Phase 2: Screenshot & Storage

    Playwright vs Selenium: Playwright is faster & more reliable. Lock to the official Docker image (mcr.microsoft.com/playwright).

    Desktop + Mobile: capture two viewports (e.g. 1200×800 & 375×667) so you can optionally report on responsiveness.

    Error Handling:

        Timeouts → return a well-formed “AnalysisPending” status so front-end can poll.

        Blocked / invalid SSL → catch and log.

    Cache Layer: simple file-based TTL cache (URL + hash → screenshot) so re-analyzing during dev doesn’t hammer Playwright.

    Cloudinary Settings:

        Tag each screenshot with project name and timestamp.

        Make results public but unlisted (signed URLs).

Phase 3: AI Analysis Engine

    Rule-Based Pre-Checks

        Run CSS/DOM parsers (e.g. cssutils or cheerio) for fonts, colors, whitespace metrics.

        Bundle those numeric metrics into your LLM prompt—this makes the LLM’s job easier and faster.

    Ollama Prompt Design

        Keep prompts < 1 k tokens: feed it a 1–2 paragraph system prompt + JSON of metrics + screenshot link.

        Test prompt “temperature” at 0.2–0.4 to keep outputs consistent.

    Fallback Path: if Ollama is down, still generate a report with “Automated metrics only” and a stubbed explanation.

Phase 4: Scoring & Report Generation

    Weights in Config: read your typography/color/layout weights from a weights.yaml.

    HTML Template + CSS

        Use Jinja2 or Mako to fill in scores, explanations, and embed image thumbnails.

        Render to PDF with WeasyPrint or Puppeteer—no need to hand-craft PDF drawing primitives.

    API Design

        Return a single analysis_id immediately.

        Front-end polls GET /analysis/{id} until status == “done” and then fetch the PDF URL.

Phase 5: Google Sheets Integration + Master Orchestrator Pattern

    **COMPLETED ✅** - Full implementation with orchestrator pattern for frontend integration

    Service Account Setup:
        - Google Cloud service account created with Sheets API access
        - JSON credentials stored in credentials/google-sheets-service-account.json
        - Authentication via google-auth + gspread libraries
        - Automatic spreadsheet creation with structured headers

    Master Orchestrator Endpoint (`/api/v1/master/analyze-complete`):
        - **Single endpoint** that orchestrates entire workflow for frontend
        - **Parallel execution**: Screenshots (desktop + mobile) captured simultaneously via asyncio.gather()
        - **Sequential dependencies**: AI analysis runs after screenshots complete
        - **Background tasks**: Cloudinary uploads + Google Sheets logging happen asynchronously
        - **Graceful degradation**: Partial success tolerance with structured error reporting

    Architecture Pattern:
        ```python
        @router.post("/api/v1/master/analyze-complete")
        async def master_analyze(url: str, background_tasks: BackgroundTasks):
            # 1) Parallel: Desktop + Mobile screenshots
            screenshot_tasks = [desktop_capture(), mobile_capture()]
            screenshots = await asyncio.gather(*screenshot_tasks, return_exceptions=True)
            
            # 2) Sequential: AI analysis (needs screenshots)  
            ai_insights = await ai_analysis_service.analyze(good_screenshots)
            
            # 3) Background: Non-critical tasks
            background_tasks.add_task(upload_and_log, data)
            
            # 4) Return: Complete structured response
            return AnalysisResult(screenshots, ai_insights, errors={})
        ```

    Response Schema:
        - `AnalysisResult` with screenshots, AI insights, upload URLs, sheet entry ID
        - Structured error handling per service (non-fatal failures don't kill workflow)
        - Frontend gets complete data in single HTTP response (no polling required)

    Google Sheets Features:
        - Automatic logging of all analysis results
        - Rich data format: scores, screenshots, AI summaries, duration
        - Thumbnail embedding via =IMAGE() formulas for visual spreadsheet
        - Batch operations for performance
        - Health checks and manual logging endpoints

    Benefits:
        - **Frontend simplicity**: Single API call (URL → complete analysis)
        - **Performance**: Parallel execution where possible  
        - **Reliability**: Continues with partial data if non-critical services fail
        - **User experience**: Immediate response with complete analysis data
        - **Monitoring**: All results automatically logged to Google Sheets for tracking

Phase 6: API Integration & Testing

    Automated Tests

        Unit: mock Cloudinary + Ollama responses.

        Integration: spin up real services in CI via Docker Compose, run end-to-end on a known static site (e.g. example.com). Assert you get back a PDF.

    Load Testing: with a small tool (e.g. locust) hit your /analyze endpoint to surface any concurrency bottlenecks early.

Phase 7: Deployment & Documentation

    Docker Compose

        Define three services: web (FastAPI), playwright, ollama.

        Expose only web port to the outside.

    Cloud Deploy

        For a “one-click” demo, use Fly.io or Railway. They’ll build your Docker image and run it with minimal config.

    Docs

        Integrate Swagger (/docs) and ReDoc (/redoc) from FastAPI.

        Provide a one-pager “How to run locally” and “How to deploy” in your README.