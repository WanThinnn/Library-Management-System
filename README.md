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

## Deployment

### Option 1: Build from Source (Development)

**Step 1: Clone Repository**

```bash
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System
```

**Step 2: Setup Environment**

```bash
chmod +x start  # Make start script executable
./start setup
```

This will:
- Check Docker and Docker Compose installation
- Verify SSL certificates exist
- Auto-detect OS and install root CA certificate
- Copy `.env.example` to `.env`

**Step 3: Build and Run**

```bash
./start build
./start up
./start makemigrations
./start migrate
./start initdata
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
chmod +x start  # Make start script executable
cp .env.example .env
nano .env  # Edit configuration
./start --prod setup
```

**Step 3: Pull and Run**

```bash
./start --prod build
./start --prod up
```

**Step 4: Initialize Database**

```bash
./start --prod makemigrations
./start --prod migrate
./start --prod initdata
```

**Step 5: Access Application**

- URL: `https://library.cyberfortress.local`
- Default Admin: `admin` / `admin123`

### Docker Hub

Pre-built image: `wanthinnn/library-management-system:latest`

```bash
docker pull wanthinnn/library-management-system:latest
```

## Quick Commands

Use the `./start` script with `--prod` or `--dev` flags:

**Note:** On Linux/macOS, you may need to use `sudo` for Docker commands:
```bash
sudo ./start build
sudo ./start --prod up
```

```bash
# Development (default)
./start build               # Build development images
./start up                  # Start development services
./start logs                # View development logs
./start migrate             # Run migrations
./start initdata            # Initialize sample data

# Production (add --prod flag)
./start --prod build        # Pull and build production
./start --prod up           # Start production services
./start --prod logs         # View production logs
./start --prod migrate      # Run migrations (production)
./start --prod initdata     # Initialize sample data (production)

# Other commands
./start help                # Show all commands
./start setup               # Initial setup (certificates, .env)
./start down [--prod]       # Stop services
./start restart [--prod]    # Restart services
./start makemigrations [--prod] # Create migrations
./start shell [--prod]      # Open Django shell
./start clean [--prod]      # Remove containers and volumes
./start rebuild [--prod]    # Clean rebuild
```

## Make Commands (Alternative)

All commands work with optional `--prod` flag for production mode:

```bash
# Development (default)
make build              # Build development images
make up                 # Start development services
make logs               # View development logs
make migrate            # Run migrations
make initdata           # Initialize sample data

# Production (add --prod flag)
make --prod build       # Pull and build production
make --prod up          # Start production services
make --prod logs        # View production logs
make --prod migrate     # Run migrations (production)
make --prod initdata    # Initialize sample data (production)

# Common commands (works with --prod flag)
make help               # Show all commands
make setup              # Initial setup (certificates, .env)
make down [--prod]      # Stop services
make restart [--prod]   # Restart services
make makemigrations [--prod] # Create migrations
make shell [--prod]     # Open Django shell
make clean [--prod]     # Remove containers and volumes
make rebuild [--prod]   # Clean rebuild
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

Edit `.env` file:

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

## Sample Data

The `./start initdata` command creates:
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
./start shell
# Then inside shell: python manage.py test
```

Or use docker compose directly:
```bash
docker compose exec web python manage.py test
```

## Production Deployment

For production deployment on a server:

**Note:** Use `sudo` for all commands on Linux servers.

```bash
# On production server
git clone https://github.com/WanThinnn/Library-Management-System.git
cd Library-Management-System

# Make start script executable
chmod +x start

# Configure environment
cp .env.example .env
nano .env  # Set DEBUG=False, strong SECRET_KEY, proper ALLOWED_HOSTS

# Deploy (use sudo on Linux)
sudo ./start --prod build
sudo ./start --prod up
sudo ./start --prod makemigrations
sudo ./start --prod migrate
sudo ./start --prod initdata
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
./start logs

# Restart services
./start restart

# Clean rebuild
./start rebuild
```

Or use sudo on Linux:
```bash
sudo ./start --prod logs
sudo ./start --prod restart
```

### Database Reset

```bash
./start clean
./start build
./start up
./start migrate
./start initdata
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
