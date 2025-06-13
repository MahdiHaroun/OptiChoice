#!/bin/bash

# Script to check Docker setup before running the container

echo "Checking Docker setup for OptiChoice..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create an .env file from .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

# Check if SQLite database exists
if [ ! -f db.sqlite3 ]; then
    echo "Warning: SQLite database file not found at db.sqlite3."
    echo "A new database will be created."
fi

# Check Docker and Docker Compose installation
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH!"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed or not in PATH!"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "Everything looks good! You can now run 'docker-compose up -d'"
exit 0
