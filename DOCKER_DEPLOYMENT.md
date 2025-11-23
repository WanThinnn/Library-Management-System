# Docker Deployment Guide

Hướng dẫn triển khai Library Management System với Docker Compose.

## Kiến trúc

- **Django**: Framework backend
- **Gunicorn**: WSGI HTTP Server (3 workers)
- **Nginx**: Reverse proxy + HTTPS
- **SQLite**: Database (lưu trong Docker volume)
- **SSL/HTTPS**: Self-signed certificates (development) hoặc Let's Encrypt (production)

## Cấu trúc Files

```
.
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Django app Docker image
├── .env.example               # Environment variables template
├── .dockerignore              # Docker ignore file
├── Makefile                   # Convenient commands
├── nginx/
│   ├── Dockerfile            # Nginx Docker image
│   ├── nginx.conf            # Main Nginx config
│   └── conf.d/
│       └── django.conf       # Django-specific config
├── scripts/
│   ├── setup.sh             # Setup script
│   └── generate-certs.sh    # SSL certificate generator
└── certs/                    # SSL certificates (generated)
    ├── cert.pem
    └── key.pem
```

## Yêu cầu

- Docker >= 20.10
- Docker Compose >= 2.0
- Make (optional, for convenience commands)

## Cài đặt & Chạy

### 1. Setup ban đầu

```bash
# Tạo SSL certificates và .env file
make setup

# Hoặc thủ công:
bash scripts/setup.sh
```

### 2. Cấu hình Environment

Chỉnh sửa file `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,yourdomain.com
DATABASE_URL=sqlite:////app/data/db.sqlite3
MAIL_SERVER_USER=your-email@gmail.com
MAIL_SERVER_PWD=your-app-password
```

### 3. Build và Start

```bash
# Build images
make build

# Start services
make up

# Hoặc thủ công:
docker-compose build
docker-compose up -d
```

### 4. Chạy Migrations

```bash
make migrate

# Hoặc:
docker-compose exec web python manage.py migrate
```

### 5. Tạo Superuser

```bash
make createsuperuser

# Hoặc:
docker-compose exec web python manage.py createsuperuser
```

### 6. Truy cập Application

- **HTTPS**: https://localhost
- **HTTP**: http://localhost (redirect to HTTPS)

## Commands thường dùng

```bash
# Xem logs
make logs

# Restart services
make restart

# Stop services
make down

# Django shell
make shell

# Collect static files
make collectstatic

# Clean all (remove containers & volumes)
make clean

# Rebuild from scratch
make rebuild
```

## Docker Volumes

Hệ thống sử dụng 2 volumes:

1. **sqlite_volume**: Lưu trữ database (`db.sqlite3`)
   - Mount point: `/app/data/db.sqlite3`
   - Persistent data được giữ ngay cả khi container bị xóa

2. **static_volume**: Lưu trữ static files
   - Mount point: `/app/staticfiles/`
   - Shared giữa Django và Nginx

### Backup Database

```bash
# Backup
docker-compose exec web sqlite3 /app/data/db.sqlite3 .dump > backup.sql

# Restore
cat backup.sql | docker-compose exec -T web sqlite3 /app/data/db.sqlite3
```

### Copy Database ra ngoài

```bash
docker cp django_app:/app/data/db.sqlite3 ./db.sqlite3.backup
```

## Production Deployment

### 1. SSL Certificates (Let's Encrypt)

Thay thế self-signed certificates bằng Let's Encrypt:

```bash
# Install certbot
sudo apt-get install certbot

# Generate certificates
sudo certbot certonly --standalone -d yourdomain.com

# Copy to certs directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./certs/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./certs/key.pem
```

### 2. Environment Settings

Update `.env` cho production:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=generate-a-strong-secret-key
```

### 3. Security Headers

Nginx đã được cấu hình với:
- HSTS (Strict-Transport-Security)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

### 4. Performance Tuning

**Gunicorn workers**: Tính theo công thức `(2 x CPU cores) + 1`

Chỉnh sửa trong `docker-compose.yml`:
```yaml
command: gunicorn ... --workers 5
```

**Nginx caching**: Đã bật cho static files (30 days)

## Troubleshooting

### Container không start

```bash
# Check logs
docker-compose logs web
docker-compose logs nginx

# Check container status
docker-compose ps
```

### Permission errors với SQLite

```bash
# Fix permissions
docker-compose exec web chmod -R 777 /app/data
```

### SSL certificate errors

```bash
# Regenerate certificates
bash scripts/generate-certs.sh

# Restart nginx
docker-compose restart nginx
```

### Static files không load

```bash
# Collect static files
make collectstatic

# Restart services
make restart
```

## Monitoring

### View logs real-time

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
```

### Check resource usage

```bash
docker stats
```

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Use trusted SSL certificates (Let's Encrypt)
- [ ] Restrict `ALLOWED_HOSTS`
- [ ] Set strong database passwords (nếu dùng PostgreSQL/MySQL)
- [ ] Enable firewall (chỉ mở port 80, 443)
- [ ] Regular backups của SQLite database
- [ ] Update Docker images thường xuyên

## Scaling

### Horizontal Scaling (Multiple Gunicorn instances)

Update `docker-compose.yml`:

```yaml
services:
  web:
    deploy:
      replicas: 3
```

### Load Balancing

Nginx đã được cấu hình sẵn upstream load balancing.

## Support

Để được hỗ trợ, vui lòng mở issue trên GitHub repository.
