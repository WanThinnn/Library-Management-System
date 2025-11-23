# Library Management System

A comprehensive library management system built with Django, featuring book cataloging, reader management, borrowing/return tracking, and detailed reporting capabilities.

## Features

- **User Management**: Multi-role authentication system (Admin, Librarian, Reader)
- **Book Management**: Complete book cataloging with categories, authors, and inventory tracking
- **Reader Management**: Reader registration and profile management with multiple reader types
- **Borrowing System**: Book borrowing and return workflow with due date tracking
- **Receipt Management**: Financial transaction tracking for library fees
- **Reports**: 
  - Borrowing statistics by category
  - Overdue books tracking
- **Parameter Configuration**: Customizable system parameters (max borrowing days, fees, etc.)

## Technology Stack

- **Backend**: Django 5.2.6
- **Web Server**: Gunicorn 21.2.0
- **Reverse Proxy**: Nginx (Alpine)
- **Database**: SQLite
- **Static Files**: WhiteNoise
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **SSL/TLS**: HTTPS with custom certificates

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- Git

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System
```

### 2. Setup Environment

```bash
make setup
```

This will:
- Check Docker and Docker Compose installation
- Verify SSL certificates
- Auto-detect OS and install root CA certificate
- Copy `.env.example` to `.env`

### 3. Build and Run

```bash
make build
make up
make migrate
make initdata
```

### 4. Access Application

- URL: `https://library.cyberfortress.local`
- Default Admin: `admin` / `admin123`

## Make Commands

```bash
make help          # Show all available commands
make setup         # Initial setup
make build         # Build Docker images
make up            # Start services
make down          # Stop services
make restart       # Restart services
make logs          # View logs
make migrate       # Run database migrations
make initdata      # Initialize sample data
make createsuperuser # Create admin user
make shell         # Open Django shell
make clean         # Remove containers and volumes
make rebuild       # Clean rebuild
```

## Project Structure

```
Library-Management-System/
├── src/
│   ├── LibraryApp/           # Main application
│   ├── LibraryManagementSystem/  # Django settings
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS files
│   ├── init_data.py          # Sample data initialization
│   └── requirements.txt      # Python dependencies
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── conf.d/
│       └── django.conf       # Nginx configuration
├── certs/                    # SSL certificates
├── scripts/
│   └── setup.sh              # Setup script
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── .env.example
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=library.cyberfortress.local,cyberfortress.local,siem-dacn.local
DATABASE_URL=sqlite:///data/db.sqlite3
```

### SSL Certificates

Place your SSL certificates in the `certs/` directory:
- `_.cyberfortress.local.crt` - SSL certificate
- `_.cyberfortress.local.key` - Private key
- `CyberFortressRootCA.crt` - Root CA certificate

### Hosts File

Add to `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```
127.0.0.1 library.cyberfortress.local
```

## Docker Hub

Pre-built images available at Docker Hub: **wanthinnn/library-management-system**

### Deployment Options

**Option 1: Git Clone (Recommended)**

```bash
# Clone repository
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System

# Setup and run
make setup
make build
make up
make migrate
make initdata
```

**Option 2: Docker Pull (Production)**

```bash
# Clone repository for config files
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Pull and run with production compose
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d

# Initialize database
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python init_data.py
```

Access at: `https://library.cyberfortress.local`  
Default credentials: `admin` / `admin123`

## Sample Data

The `make initdata` command creates:
- 1 Admin user (admin/admin123)
- 5 System parameters
- 3 Reader types
- 8 Book categories
- 24 Authors
- 11 Books with inventory
- 5 Sample readers

## Development

### Local Development

```bash
cd src
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python init_data.py
python manage.py runserver
```

### Run Tests

```bash
docker compose exec web python manage.py test
```

## Production Deployment

### Server Deployment

```bash
# On server
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System
sudo make setup
sudo make build
sudo make up
sudo make migrate
sudo make initdata
```

### Using Docker Hub Image

Update `docker-compose.yml`:

```yaml
services:
  web:
    image: wanthinnn/library-management-system:latest
    # Remove build section
```

Then:

```bash
docker compose pull
docker compose up -d
```

## CI/CD

GitHub Actions automatically builds and pushes Docker images to Docker Hub on every push to `main` branch.

### Setup Secrets

Add to GitHub repository secrets:
- `DOCKERHUB_TOKEN` - Docker Hub access token

## Troubleshooting

### Container Issues

```bash
# View logs
make logs

# Restart services
make restart

# Clean rebuild
make rebuild
```

### Database Reset

```bash
make clean
make build
make up
make migrate
make initdata
```

### SSL Certificate Issues

Ensure root CA is installed:

```bash
# Linux
sudo cp certs/CyberFortressRootCA.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Windows
certutil -addstore ROOT certs\CyberFortressRootCA.crt

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain certs/CyberFortressRootCA.crt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

- WanThinnn - Initial work

## Acknowledgments

- University of Information Technology (UIT)
- SE104 - Software Engineering Course
