# SSL Certificates Information

## Certificates đã được cấu hình

Project đã có sẵn SSL certificates từ CyberFortress CA:

### Files:
1. **`_.cyberfortress.local.crt`** - Server Certificate
   - Domain: `cyberfortress.local`, `*.cyberfortress.local`, `siem-dacn.local`, `*.siem-dacn.local`
   - Valid: June 11, 2025 - June 11, 2026
   - Type: EC (Elliptic Curve) Certificate

2. **`_.cyberfortress.local.key`** - Private Key
   - EC Private Key for server certificate

3. **`CyberFortress-RootCA.crt`** - Root CA Certificate
   - Issuer: CyberFortress-RootCA
   - Valid: June 11, 2025 - June 09, 2035 (10 years)

## Cấu hình đã áp dụng

### Nginx Configuration
```nginx
ssl_certificate /etc/nginx/certs/_.cyberfortress.local.crt;
ssl_certificate_key /etc/nginx/certs/_.cyberfortress.local.key;
ssl_trusted_certificate /etc/nginx/certs/CyberFortress-RootCA.crt;
```

### Supported Domains
- `cyberfortress.local`
- `*.cyberfortress.local` (wildcard)
- `siem-dacn.local`
- `*.siem-dacn.local` (wildcard)
- `localhost` (fallback)

## Sử dụng

### 1. Cấu hình hosts file (Windows)

Mở file `C:\Windows\System32\drivers\etc\hosts` với quyền Administrator và thêm:

```
127.0.0.1    cyberfortress.local
127.0.0.1    www.cyberfortress.local
127.0.0.1    siem-dacn.local
127.0.0.1    www.siem-dacn.local
```

### 2. Import Root CA vào Trusted Root Certificates (Windows)

**Option 1: Double-click certificate**
1. Double-click `CyberFortress-RootCA.crt`
2. Click "Install Certificate"
3. Select "Local Machine"
4. Choose "Place all certificates in the following store"
5. Browse → Select "Trusted Root Certification Authorities"
6. Click "Next" → "Finish"

**Option 2: Using certutil (Command line)**
```powershell
# Run as Administrator
certutil -addstore -f "ROOT" "d:\Documents\UIT\Nam_4\SE104_CNPM\Library-Management-System\certs\CyberFortress-RootCA.crt"
```

### 3. Truy cập application

Sau khi cấu hình:
- https://cyberfortress.local
- https://www.cyberfortress.local
- https://siem-dacn.local
- https://localhost

## Docker Compose

Certificates đã được mount vào Nginx container:

```yaml
volumes:
  - ./certs:/etc/nginx/certs:ro
```

## Security Notes

### Certificate Details:
- **Algorithm**: ECDSA (Elliptic Curve)
- **Key Size**: 384-bit (equivalent to ~7680-bit RSA)
- **Hash Algorithm**: SHA-384
- **SSL Protocols**: TLSv1.2, TLSv1.3
- **OCSP Stapling**: Enabled

### Best Practices Applied:
✅ Strong encryption (EC P-384)
✅ Modern TLS protocols only
✅ HSTS enabled (Strict-Transport-Security)
✅ OCSP Stapling for certificate validation
✅ Secure cipher suites
✅ Root CA for trust chain

## Troubleshooting

### Browser shows "Not Secure"
→ Import Root CA certificate vào Trusted Root (xem bước 2)

### Certificate name mismatch
→ Kiểm tra hosts file và đảm bảo truy cập đúng domain

### Certificate expired
→ Certificate valid đến June 11, 2026. Renew trước ngày đó.

## Renewal (Khi hết hạn)

Contact CyberFortress CA để renew certificate hoặc tạo certificate mới với cùng domains.

---

**Note**: Certificates này là production-ready và an toàn hơn self-signed certificates thông thường.
