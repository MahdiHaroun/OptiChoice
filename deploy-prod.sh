#!/bin/bash

# Production deployment script for OPC Django application
# This script performs a full production deployment

set -e

APP_DIR="/opt/opc"
COMPOSE_FILE="docker-compose.prod.yml"

echo "Starting production deployment process..."

# Navigate to app directory
cd $APP_DIR

# Load the new Docker image
if [ -f "django.tar" ]; then
    echo "Loading Django Docker image..."
    docker load < django.tar
    echo "Docker image loaded successfully"
else
    echo "Django Docker image not found!"
    exit 1
fi

# Stop all services
echo "Stopping all services..."
docker-compose -f $COMPOSE_FILE down

# Remove unused images and containers
echo "Cleaning up unused Docker resources..."
docker system prune -f

# Start web service
echo "Starting web service..."
docker-compose -f $COMPOSE_FILE up -d web

# Wait for web service to be ready
echo "Waiting for web service to be ready..."
sleep 20

# Start nginx
echo "Starting nginx..."
docker-compose -f $COMPOSE_FILE up -d nginx

# Clean up tar files
rm -f django.tar

# Show running containers
echo "Current running containers:"
docker-compose -f $COMPOSE_FILE ps

# Check if services are healthy
echo "Checking service health..."
sleep 10
docker-compose -f $COMPOSE_FILE logs --tail=20 web
docker-compose -f $COMPOSE_FILE logs --tail=20 nginx

echo "Production deployment completed successfully!"
