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

Phase 5: Google Sheets Integration

    Service Account: store the JSON key as a secret; use google-auth + gspread for simplicity.

    Batch Writes: if you ever process more than one URL in one run, append them in bulk—faster and fewer API calls.

    Thumbnail Embedding: use the Sheets =IMAGE("…") formula in your payload so your sheet shows the screenshot inline.

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