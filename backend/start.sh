#!/bin/bash

# Website Design Scorer - Docker Startup Script

echo "🚀 Starting Website Design Scorer with Ollama + Llama3"
echo "=================================================="

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker first."
        exit 1
    fi
    echo "✅ Docker is running"
}

# Function to check if docker-compose is available
check_compose() {
    if command -v docker-compose > /dev/null 2>&1; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version > /dev/null 2>&1; then
        COMPOSE_CMD="docker compose"
    else
        echo "❌ Docker Compose is not available"
        exit 1
    fi
    echo "✅ Docker Compose found: $COMPOSE_CMD"
}

# Main execution
main() {
    check_docker
    check_compose
    
    echo ""
    echo "🔧 Building and starting services..."
    
    # Stop any existing containers
    $COMPOSE_CMD down
    
    # Build and start services
    $COMPOSE_CMD up --build -d
    
    echo ""
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check service status
    echo ""
    echo "📊 Service Status:"
    echo "=================="
    $COMPOSE_CMD ps
    
    echo ""
    echo "🔍 Checking Ollama health..."
    
    # Wait for Ollama to be ready
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "✅ Ollama is ready!"
            break
        else
            echo "⏳ Waiting for Ollama... (attempt $attempt/$max_attempts)"
            sleep 5
            attempt=$((attempt + 1))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ Ollama failed to start within expected time"
        echo "Check logs with: $COMPOSE_CMD logs ollama"
        exit 1
    fi
    
    echo ""
    echo "🧠 Checking Llama3 model..."
    
    # Check if Llama3 model is available
    if curl -s http://localhost:11434/api/tags | grep -q "llama3"; then
        echo "✅ Llama3 model is available!"
    else
        echo "⏳ Llama3 model not found, checking init service..."
        $COMPOSE_CMD logs ollama-init | tail -10
    fi
    
    echo ""
    echo "🌐 Checking Backend API..."
    
    # Wait for backend to be ready
    max_attempts=20
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
            echo "✅ Backend API is ready!"
            break
        else
            echo "⏳ Waiting for Backend API... (attempt $attempt/$max_attempts)"
            sleep 3
            attempt=$((attempt + 1))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ Backend API failed to start"
        echo "Check logs with: $COMPOSE_CMD logs backend"
        exit 1
    fi
    
    echo ""
    echo "🎉 All services are ready!"
    echo "========================="
    echo "📡 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "🧠 Ollama: http://localhost:11434"
    echo "🔍 Analysis Health: http://localhost:8000/api/v1/analysis/health"
    echo ""
    echo "🛠️  Useful commands:"
    echo "View logs: $COMPOSE_CMD logs -f"
    echo "Stop services: $COMPOSE_CMD down"
    echo "Restart: $COMPOSE_CMD restart"
    echo ""
    echo "Ready to analyze websites! 🚀"
}

# Handle script arguments
case "${1:-}" in
    "stop")
        echo "🛑 Stopping all services..."
        check_compose
        $COMPOSE_CMD down
        echo "✅ All services stopped"
        ;;
    "restart")
        echo "🔄 Restarting services..."
        check_compose
        $COMPOSE_CMD restart
        echo "✅ Services restarted"
        ;;
    "logs")
        check_compose
        $COMPOSE_CMD logs -f
        ;;
    "status")
        check_compose
        $COMPOSE_CMD ps
        ;;
    *)
        main
        ;;
esac
