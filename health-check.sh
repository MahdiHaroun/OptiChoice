#!/bin/bash

# Health check script for OptiChoice deployment

APP_URL="http://134.122.70.184:8000"
APP_DIR="/app/optichoice"

echo "=== OptiChoice Health Check ==="
echo "Timestamp: $(date)"
echo

# Check if Docker is running
if ! systemctl is-active --quiet docker; then
    echo "❌ Docker is not running"
    exit 1
else
    echo "✅ Docker is running"
fi

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "❌ App directory $APP_DIR does not exist"
    exit 1
else
    echo "✅ App directory exists"
fi

# Check if containers are running
cd $APP_DIR
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ Containers are running"
else
    echo "❌ Containers are not running"
    echo "Container status:"
    docker-compose -f docker-compose.prod.yml ps
    exit 1
fi

# Check if application responds
if curl -f -s "$APP_URL" > /dev/null; then
    echo "✅ Application is responding"
else
    echo "❌ Application is not responding"
    echo "Checking container logs:"
    docker-compose -f docker-compose.prod.yml logs --tail=10
    exit 1
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "⚠️  Disk usage is high: ${DISK_USAGE}%"
else
    echo "✅ Disk usage is normal: ${DISK_USAGE}%"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ "$MEM_USAGE" -gt 80 ]; then
    echo "⚠️  Memory usage is high: ${MEM_USAGE}%"
else
    echo "✅ Memory usage is normal: ${MEM_USAGE}%"
fi

echo
echo "=== Health Check Complete ==="
echo "Application URL: $APP_URL"
