#!/bin/bash

# Website Design Scorer - Quick Start Script
# Phase 3 AI Analysis Engine

echo "🚀 Website Design Scorer - Quick Start"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker found"

# Navigate to backend directory
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found. Please run this script from the project root."
    exit 1
fi

cd backend

# Check if .env file exists, if not create from template
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env file from template..."
        cp .env.example .env
        echo "⚠️  Please edit backend/.env with your Cloudinary credentials"
    else
        echo "❌ .env.example not found"
        exit 1
    fi
fi

echo "🐳 Starting Docker services..."

# Build and start services
docker compose build
if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker compose ps

# Test API health
echo "🏥 Testing API health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null; then
        echo "✅ Backend API is ready!"
        break
    fi
    echo "   Waiting for backend... ($i/30)"
    sleep 2
done

# Test Ollama
echo "🤖 Testing Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama service is ready!"
else
    echo "⚠️  Ollama service starting up (Llama3 model downloading...)"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📡 API Endpoints:"
echo "   Health Check: http://localhost:8000/api/v1/health"
echo "   API Docs:     http://localhost:8000/docs"
echo ""
echo "🧪 Test the system:"
echo "   cd backend && python test_analysis.py"
echo ""
echo "📝 View logs:"
echo "   docker compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker compose down"
echo ""

# Check if Llama3 model is downloaded
echo "🔍 Checking Llama3 model status..."
if docker compose exec ollama ollama list | grep -q "llama3"; then
    echo "✅ Llama3 model is ready!"
    echo ""
    echo "🚀 Ready for AI analysis!"
else
    echo "⏳ Llama3 model still downloading (~4.7GB)"
    echo "   Check progress: docker compose logs ollama-init"
    echo "   This may take 5-10 minutes depending on your internet speed"
fi

echo ""
echo "🎯 Phase 3 AI Analysis Engine is operational!"
