# 🚀 Quick Start - Docker Deployment

## Bước 1: Chuẩn bị môi trường

```bash
# Copy environment file
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
nano .env
```

## Bước 2: Cấu hình SSL Certificates

### ✅ Certificates đã sẵn sàng!

Project đã có SSL certificates từ CyberFortress CA trong thư mục `certs/`:
- `_.cyberfortress.local.crt` - Server certificate
- `_.cyberfortress.local.key` - Private key
- `CyberFortress-RootCA.crt` - Root CA

### Import Root CA (để browser tin tưởng)

**Windows:**
```powershell
# Run PowerShell as Administrator
certutil -addstore -f "ROOT" "d:\Documents\UIT\Nam_4\SE104_CNPM\Library-Management-System\certs\CyberFortress-RootCA.crt"
```

Hoặc double-click `CyberFortress-RootCA.crt` → Install Certificate → Local Machine → Trusted Root Certification Authorities

### Cấu hình hosts file

Mở `C:\Windows\System32\drivers\etc\hosts` với quyền Administrator và thêm:
```
127.0.0.1    cyberfortress.local
127.0.0.1    www.cyberfortress.local
127.0.0.1    siem-dacn.local
```

## Bước 3: Build và Run

```bash
# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## Bước 4: Chạy Migrations & Create Admin

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files (nếu cần)
docker-compose exec web python manage.py collectstatic --noinput
```

## Bước 5: Truy cập Application

- **HTTPS**: https://cyberfortress.local (hoặc https://localhost)
- **Admin**: https://cyberfortress.local/admin

**Supported domains:**
- https://cyberfortress.local
- https://www.cyberfortress.local
- https://siem-dacn.local
- https://localhost

## Các lệnh hữu ích

```bash
# Xem logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Remove everything (bao gồm volumes)
docker-compose down -v

# Django shell
docker-compose exec web python manage.py shell

# Backup database
docker cp django_app:/app/data/db.sqlite3 ./backup_$(date +%Y%m%d).sqlite3
```

## Troubleshooting

### Lỗi SSL Certificate
```bash
# Tạo lại certificates
bash scripts/generate-certs.sh
docker-compose restart nginx
```

### Lỗi Permission với SQLite
```bash
docker-compose exec web chmod -R 777 /app/data
docker-compose restart web
```

### Port 80/443 đã được sử dụng
```bash
# Kiểm tra process đang dùng port
netstat -ano | findstr :80
netstat -ano | findstr :443

# Stop process hoặc đổi port trong docker-compose.yml
```

## Production Checklist

- [ ] Thay đổi `SECRET_KEY` trong `.env`
- [ ] Set `DEBUG=False`
- [ ] Cập nhật `ALLOWED_HOSTS`
- [ ] Dùng SSL certificate thật (Let's Encrypt)
- [ ] Backup database định kỳ
- [ ] Monitor logs và resource usage
- [ ] Cấu hình firewall

---

📖 Xem chi tiết: [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
