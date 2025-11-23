#!/bin/bash

# Setup script for Docker deployment

echo "=== Library Management System - Docker Setup ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration before continuing."
    echo ""
fi

# Generate SSL certificates
echo "Checking SSL certificates..."
if [ ! -f ./certs/cert.pem ] || [ ! -f ./certs/key.pem ]; then
    echo "SSL certificates not found. Generating self-signed certificates..."
    bash scripts/generate-certs.sh
else
    echo "SSL certificates already exist."
fi

echo ""
echo "=== Setup completed! ==="
echo ""
echo "Next steps:"
echo "1. Review and update .env file with your settings"
echo "2. Run: docker-compose build"
echo "3. Run: docker-compose up -d"
echo "4. Access the application at https://localhost"
echo ""
echo "For production, replace self-signed certificates with trusted ones."
