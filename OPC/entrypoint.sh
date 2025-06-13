#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn OPC.wsgi:application --bind 0.0.0.0:8000
