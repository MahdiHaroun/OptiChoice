#!/bin/bash

# Deployment script for OPC Django application
# This script should be run on the production server

set -e

APP_DIR="/opt/opc"
COMPOSE_FILE="docker-compose.prod.yml"

echo "Starting deployment process..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

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

# Check if it's a full deployment
if [ "$1" == "full" ]; then
    echo "Performing full deployment..."
    
    # Stop all services
    docker-compose -f $COMPOSE_FILE down
    
    # Remove unused images and containers
    docker system prune -f
    
    # Start all services
    docker-compose -f $COMPOSE_FILE up -d
    
    echo "Full deployment completed!"
else
    echo "Performing targeted deployment..."
    
    # Update only the web service
    docker-compose -f $COMPOSE_FILE up -d --no-deps web
    
    # Ensure nginx is running
    docker-compose -f $COMPOSE_FILE up -d --no-deps nginx
    
    echo "Targeted deployment completed!"
fi

# Clean up tar files
rm -f django.tar

# Show running containers
echo "Current running containers:"
docker-compose -f $COMPOSE_FILE ps

echo "Deployment process completed successfully!"
