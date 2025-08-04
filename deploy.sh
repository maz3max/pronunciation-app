#!/bin/bash

# Production deployment script for phonetics app

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Create logs directory
mkdir -p logs

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Start the application
echo "▶️ Starting application..."
docker-compose up -d

# Wait for health check
echo "🏥 Waiting for health check..."
sleep 10

# Check if the application is running
HEALTH_URL="http://localhost:8000"

for i in {1..30}; do
    if curl -f -s "$HEALTH_URL" > /dev/null; then
        echo "✅ Application is running successfully!"
        break
    else
        echo "⏳ Waiting for application to start... ($i/30)"
        sleep 2
    fi
    
    if [ $i -eq 30 ]; then
        echo "❌ Application failed to start within timeout"
        docker-compose logs
        exit 1
    fi
done

echo "🎉 Deployment completed successfully!"
echo "📊 Application logs: docker-compose logs -f"
echo "🌐 Access the application at: $HEALTH_URL"
