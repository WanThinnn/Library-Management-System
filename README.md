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


## Configuration

### Environment Variables

Edit `.env` file:
```bash
cp .env.example .env
```

```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=library.cyberfortress.local,127.0.0.1
DATABASE_URL=sqlite:///data/db.sqlite3
```

### SSL Certificates

Place your SSL certificates in the `certs/` directory:
- `_.cyberfortress.local.crt` - SSL certificate
- `_.cyberfortress.local.key` - Private key
- `CyberFortress-RootCA.crt` - Root CA certificate

Local development certificates:
- Any OS: `python scripts/generate.py`

### Hosts File

Add to `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```
127.0.0.1 library.cyberfortress.local
```


## Deployment

Run everything from the repository root with `python start.py ...`; it auto-selects the PowerShell script on Windows and the bash script on Linux/macOS.

### Option 1: Build from Source (Development)

**Step 1: Clone Repository**

```bash
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System
```

**Step 2: Setup Environment**

```bash
python start.py setup   # or: py start.py setup on Windows
```

This will:
- Check Docker and Docker Compose installation
- Verify SSL certificates exist
- Auto-detect OS and install root CA certificate

**Step 3: Build and Run**

```bash
python start.py build
python start.py up
python start.py makemigrations
python start.py migrate
python start.py initdata
```

**Step 4: Access Application**

- URL: `https://library.cyberfortress.local`
- Default Admin: `admin` / `admin123`

### Option 2: Use Pre-built Image (Production)

**Step 1: Clone Repository for Configuration**

```bash
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System
```

**Step 2: Configure Environment**

```bash
python start.py --prod setup
```

**Step 3: Pull and Run**

```bash
python start.py --prod build
python start.py --prod up
```

**Step 4: Initialize Database**

```bash
python start.py --prod makemigrations
python start.py --prod migrate
python start.py --prod initdata
```

**Step 5: Access Application**

- URL: `https://library.cyberfortress.local`
- Default Admin: `admin` / `admin123`

### Docker Hub

Pre-built image: `wanthinnn/library-management-system:latest`

```bash
# Pull latest image
docker pull wanthinnn/library-management-system:latest
```

## Quick Commands

Use `python start.py` with `--prod` or `--dev` (default dev). On Linux/macOS you may need `sudo` before the command if Docker requires it.

```bash
# Development (default)
python start.py build               # Build development images
python start.py up                  # Start development services
python start.py logs                # View development logs
python start.py migrate             # Run migrations
python start.py initdata            # Initialize sample data

# Production (add --prod flag)
python start.py --prod build        # Pull and build production
python start.py --prod up           # Start production services
python start.py --prod logs         # View production logs
python start.py --prod migrate      # Run migrations (production)
python start.py --prod initdata     # Initialize sample data (production)

# Other commands
python start.py help                # Show all commands
python start.py setup               # Initial setup (certificates, .env)
python start.py down [--prod/--dev]       # Stop services
python start.py restart [--prod/--dev]    # Restart services
python start.py makemigrations [--prod/--dev] # Create migrations
python start.py shell [--prod/--dev]      # Open Django shell
python start.py clean [--prod/--dev]      # Remove containers and volumes
python start.py rebuild [--prod/--dev]    # Clean rebuild
```

## Project Structure

```
Library-Management-System/
|-- start.py                  # OS-aware entrypoint
|-- docker-compose.yml
|-- docker-compose.prod.yml
|-- Dockerfile
|-- certs/                    # SSL certificates
|-- scripts/
|   |-- setup.py              # Cross-platform setup
|   |-- generate.py           # Dev cert generator (OpenSSL required)
|-- src/
|   |-- LibraryApp/           # Main application
|   |-- LibraryManagementSystem/  # Django settings
|   |-- templates/            # HTML templates
|   |-- static/               # CSS, JS files
|   |-- init_data.py          # Sample data initialization
|   |-- requirements.txt      # Python dependencies
|-- nginx/
|   |-- Dockerfile
|   |-- nginx.conf
|   |-- conf.d/
|       |-- django.conf       # Nginx configuration
|-- Makefile
|-- .env.example
```

## Sample Data

The `python start.py initdata` command creates:
- 1 Admin user (admin/admin123)
- 5 System parameters
- 3 Reader types
- 8 Book categories
- 24 Authors
- 11 Books with inventory
- 5 Sample readers


## CI/CD

GitHub Actions automatically builds and pushes Docker images to Docker Hub on every push to `main` branch.

### Setup Secrets

Add to GitHub repository secrets:
- `DOCKERHUB_TOKEN` - Docker Hub access token

## Troubleshooting

### Container Issues

```bash
# View logs
python start.py logs

# Restart services
python start.py restart

# Clean rebuild
python start.py rebuild
```

Or use sudo on Linux:
```bash
sudo python start.py --prod logs
sudo python start.py --prod restart
```

### Database Reset

```bash
python start.py clean
python start.py build
python start.py up
python start.py migrate
python start.py initdata
```

### SSL Certificate Issues

Ensure root CA is installed:

```bash
# Linux
sudo cp certs/CyberFortress-RootCA.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Windows
certutil -addstore ROOT certs\CyberFortress-RootCA.crt

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain certs/CyberFortress-RootCA.crt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors
- **Lại Quan Thiên** - [WanThinnn](https://github.com/WanThinnn)
- **Hồ Diệp Huy** - [hohuyy](https://github.com/hohuyy)

## Acknowledgments

- University of Information Technology (UIT)
- SE104 - Software Engineering Course
