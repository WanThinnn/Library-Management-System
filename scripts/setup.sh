#!/bin/bash

# Setup script for Docker deployment

echo "=== Library Management System - Docker Setup ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed (support both v1 and v2)
if ! (command -v docker-compose &> /dev/null || docker compose version &> /dev/null); then
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

# Check SSL certificates
echo "Checking SSL certificates..."
if [ -f ./certs/_.cyberfortress.local.crt ] && [ -f ./certs/_.cyberfortress.local.key ] && [ -f ./certs/CyberFortress-RootCA.crt ]; then
    echo "SSL certificates found:"
    echo "   - _.cyberfortress.local.crt"
    echo "   - _.cyberfortress.local.key"
    echo "   - CyberFortress-RootCA.crt"
else
    echo "Error: SSL certificates not found in ./certs/"
    echo "Please ensure the following files exist:"
    echo "   - certs/_.cyberfortress.local.crt"
    echo "   - certs/_.cyberfortress.local.key"
    echo "   - certs/CyberFortress-RootCA.crt"
    exit 1
fi

echo ""
echo "Install Root CA certificate on client machines:"
echo "   Windows: certutil -addstore -f ROOT certs/CyberFortress-RootCA.crt"
echo "   Linux: sudo cp certs/CyberFortress-RootCA.crt /usr/local/share/ca-certificates/ && sudo update-ca-certificates"
echo ""
echo "=== Setup completed! ==="
echo ""
echo "Next steps:"
echo "1. Review and update .env file with your settings"
echo "2. Install Root CA: certutil -addstore -f ROOT certs/CyberFortress-RootCA.crt (Windows)"
echo "3. Run: docker compose build"
echo "4. Run: docker compose up -d"
echo "5. Run: docker compose exec web python manage.py migrate"
echo "6. Run: docker compose exec web python init_data.py"
echo "7. Access the application at https://library.cyberfortress.local"
echo ""
echo "📌 Login credentials: admin / admin123"
echo ""
