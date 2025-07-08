#!/bin/bash

# Health check script for OPC Django application
# This script checks if the application is running properly

set -e

APP_DIR="/opt/opc"
COMPOSE_FILE="docker-compose.prod.yml"

echo "Checking application health..."

# Navigate to app directory
cd $APP_DIR

# Check if docker-compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Docker Compose file not found!"
    exit 1
fi

# Check if containers are running
echo "Checking container status..."
docker-compose -f $COMPOSE_FILE ps

# Check web service health
echo "Checking web service..."
if docker-compose -f $COMPOSE_FILE exec -T web python manage.py check; then
    echo "✓ Web service is healthy"
else
    echo "✗ Web service has issues"
    exit 1
fi

# Check database connection
echo "Checking database connection..."
if docker-compose -f $COMPOSE_FILE exec -T web python manage.py check --database default; then
    echo "✓ Database connection is healthy"
else
    echo "✗ Database connection has issues"
    exit 1
fi

# Check nginx
echo "Checking nginx..."
if docker-compose -f $COMPOSE_FILE exec -T nginx nginx -t; then
    echo "✓ Nginx configuration is valid"
else
    echo "✗ Nginx configuration has issues"
    exit 1
fi

# Check HTTP response
echo "Checking HTTP response..."
if curl -f http://localhost/health/ > /dev/null 2>&1; then
    echo "✓ HTTP response is healthy"
else
    echo "✗ HTTP response has issues"
    exit 1
fi

echo "All health checks passed!"
