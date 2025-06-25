#!/bin/bash

# Quick production deployment script
# This script deploys the OptiChoice application using production settings

set -e

echo "=== OptiChoice Production Deployment ==="

# Change to OPC directory
cd /home/fares-quiqflow/OPC2/OPC

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Build and start with production environment
echo "Building and starting application with production environment..."
docker-compose -f docker-compose.prod.yml up -d --build

# Show logs
echo "Deployment complete! Showing logs..."
docker-compose -f docker-compose.prod.yml logs --tail=20

# Show status
echo
echo "=== Deployment Status ==="
docker-compose -f docker-compose.prod.yml ps

echo
echo "Application is running at:"
echo "- http://localhost:8000"
echo "- http://134.122.70.184:8000"

# Health check
echo
echo "Performing health check..."
sleep 5
if curl -f -s http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "⚠️  Health check failed - check logs above"
fi
