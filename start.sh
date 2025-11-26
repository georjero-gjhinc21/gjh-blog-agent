#!/bin/bash
# GJH Blog Agent - Startup Script

set -e

echo "================================"
echo "GJH Consulting Blog Agent"
echo "================================"
echo ""

# Check if Ollama is running
echo "Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✓ Ollama is running"
else
    echo "✗ Ollama is not running. Please start Ollama first."
    echo "  Run: ollama serve"
    exit 1
fi

# Start infrastructure
echo ""
echo "Starting infrastructure..."
docker compose up -d postgres redis

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check PostgreSQL
echo "Checking PostgreSQL..."
if docker compose exec -T postgres pg_isready -U gjh_admin > /dev/null 2>&1; then
    echo "✓ PostgreSQL is ready"
else
    echo "✗ PostgreSQL is not ready yet. Waiting..."
    sleep 5
fi

# Check Redis
echo "Checking Redis..."
if docker compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis is ready"
else
    echo "✗ Redis connection failed"
fi

echo ""
echo "================================"
echo "Infrastructure is ready!"
echo "================================"
echo ""
echo "Available commands:"
echo "  ./venv/bin/python main.py workflow      - Generate a blog post"
echo "  ./venv/bin/python main.py discover      - Discover new topics"
echo "  ./venv/bin/python main.py list-posts    - List all posts"
echo "  ./venv/bin/python main.py stats         - View statistics"
echo ""
echo "To start automated scheduling:"
echo "  docker compose up -d celery-worker celery-beat"
echo ""
