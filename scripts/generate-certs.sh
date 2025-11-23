#!/bin/bash

# Script to generate self-signed SSL certificates for development
# For production, use Let's Encrypt or a trusted CA

CERTS_DIR="./certs"
DAYS=365

echo "Generating self-signed SSL certificates..."

# Create certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

# Generate private key and certificate
openssl req -x509 -nodes -days $DAYS -newkey rsa:2048 \
    -keyout "$CERTS_DIR/key.pem" \
    -out "$CERTS_DIR/cert.pem" \
    -subj "/C=VN/ST=HoChiMinh/L=HoChiMinh/O=Library/OU=IT/CN=localhost"

# Set permissions
chmod 600 "$CERTS_DIR/key.pem"
chmod 644 "$CERTS_DIR/cert.pem"

echo "SSL certificates generated successfully in $CERTS_DIR"
echo "Note: These are self-signed certificates for development only."
echo "For production, use Let's Encrypt or a trusted Certificate Authority."
