#!/bin/bash

# Deployment script for OptiChoice on Digital Ocean
# This script should be run on the server

set -e

APP_DIR="/app/optichoice"

echo "Deploying OptiChoice locally..."

# Create app directory
mkdir -p $APP_DIR
cd $APP_DIR

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# No need to pull image - we'll build locally

# Create production environment file
cat > .env.prod << 'EOF'
# Django Settings
SECRET_KEY=django-insecure-nrwvf&1*5e0h$^%zy9&1uajyym2%wh*=!%i14u%%v!2ed4v1_)
DEBUG=False
ALLOWED_HOSTS=134.122.70.184,optichoice.com,www.optichoice.com

# Database Settings (for SQLite, no credentials needed, but ready for PostgreSQL/MySQL)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mahdiharoun44@gmail.com
EMAIL_HOST_PASSWORD=ukpb cfzn eeky tnzo
DEFAULT_FROM_EMAIL=OptiChoice <mahdiharoun44@gmail.com>

# CORS Settings (for React frontend)
CORS_ALLOWED_ORIGINS=http://134.122.70.184:3000,https://optichoice.com,https://www.optichoice.com
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
JWT_ALGORITHM=HS256

# Security Settings
SESSION_COOKIE_AGE=1209600
EOF

# Create docker-compose.prod.yml
cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  web:
    build: .
    command: ./entrypoint.sh
    volumes:
      - ./db.sqlite3:/app/db.sqlite3
      - ./static:/app/static
      - ./media:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env.prod
    restart: always
    environment:
      - PYTHONUNBUFFERED=1
      - DEBUG=False
      - ALLOWED_HOSTS=134.122.70.184,optichoice.com,www.optichoice.com
EOF

# Start the application
echo "Starting the application..."
docker-compose -f docker-compose.prod.yml up -d

# Show logs
echo "Deployment complete! Showing logs..."
docker-compose -f docker-compose.prod.yml logs --tail=50

# Clean up old images
echo "Cleaning up old images..."
docker image prune -f

echo "Application is now running at http://134.122.70.184:8000"
