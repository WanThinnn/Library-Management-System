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
    echo ""
    
    # Auto-install Root CA based on OS
    echo "Installing Root CA certificate..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Detected: Linux"
        if [ -d "/usr/local/share/ca-certificates" ]; then
            sudo cp certs/CyberFortress-RootCA.crt /usr/local/share/ca-certificates/CyberFortress-RootCA.crt
            sudo update-ca-certificates
            echo "Root CA installed successfully on Linux"
        else
            echo "Could not find ca-certificates directory. Manual installation required."
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows (Git Bash, Cygwin, etc)
        echo "Detected: Windows"
        certutil -addstore -f "ROOT" "certs/CyberFortress-RootCA.crt" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Root CA installed successfully on Windows"
        else
            echo "Please run as Administrator or install manually:"
            echo "   certutil -addstore -f ROOT certs/CyberFortress-RootCA.crt"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Detected: macOS"
        sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain certs/CyberFortress-RootCA.crt
        if [ $? -eq 0 ]; then
            echo "Root CA installed successfully on macOS"
        else
            echo "Manual installation required:"
            echo "   sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain certs/CyberFortress-RootCA.crt"
        fi
    else
        echo "Unknown OS. Manual installation required:"
        echo "   Windows: certutil -addstore -f ROOT certs/CyberFortress-RootCA.crt"
        echo "   Linux: sudo cp certs/CyberFortress-RootCA.crt /usr/local/share/ca-certificates/ && sudo update-ca-certificates"
        echo "   macOS: sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain certs/CyberFortress-RootCA.crt"
    fi
else
    echo "Error: SSL certificates not found in ./certs/"
    echo "Please ensure the following files exist:"
    echo "   - certs/_.cyberfortress.local.crt"
    echo "   - certs/_.cyberfortress.local.key"
    echo "   - certs/CyberFortress-RootCA.crt"
    exit 1
fi

echo ""
echo "=== Setup completed! ==="
echo ""
echo "Next steps:"
echo "1. Review and update .env file with your settings"
echo "2. Run: docker compose build"
echo "3. Run: docker compose up -d"
echo "4. Run: docker compose exec web python manage.py migrate"
echo "5. Run: docker compose exec web python init_data.py"
echo "6. Access the application at https://library.cyberfortress.local"
echo ""
echo "Login credentials: admin / admin123"
echo ""
