#!/bin/bash
# Website Design Scorer Backend - Start Script

echo "🚀 Starting Website Design Scorer Backend..."

# Check if we're in Docker or local environment
if [ -f /.dockerenv ]; then
    echo "📦 Running in Docker container"
    PYTHON_CMD="python"
else
    echo "💻 Running in local environment"
    PYTHON_CMD="python3"
fi

# Check if virtual environment exists and activate if needed
if [ -d "venv" ] && [ ! -f /.dockerenv ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if needed (only in local environment)
if [ ! -f /.dockerenv ]; then
    echo "📦 Installing dependencies..."
    pip install -e .
fi

# Run startup checks
echo "🔍 Running startup checks..."
$PYTHON_CMD startup.py

if [ $? -ne 0 ]; then
    echo "❌ Startup checks failed. Please check your configuration."
    exit 1
fi

# Start the application
echo "🎯 Starting FastAPI application..."
if [ "$DEBUG" = "true" ]; then
    echo "🐛 Debug mode enabled"
    exec $PYTHON_CMD -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "🚀 Production mode"
    exec $PYTHON_CMD -m uvicorn main:app --host 0.0.0.0 --port 8000
fi
