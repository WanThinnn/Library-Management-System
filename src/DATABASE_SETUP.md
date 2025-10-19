# Hướng dẫn tạo Database cho Hệ thống Quản lý Thư viện

## 📋 Các bước thực hiện:

### 1. Tạo migrations
```bash
python manage.py makemigrations LibraryApp
```

### 2. Chạy migrations để tạo database tables
```bash
python manage.py migrate
```

### 3. Tạo dữ liệu mẫu (tùy chọn)
```bash
python manage.py shell < seed_data.py
```

Hoặc chạy từng dòng trong Django shell:
```bash
python manage.py shell
```
Rồi copy nội dung file `seed_data.py` vào.

## 📊 Cấu trúc Database đã tạo:

### 1. **Parameter** (Tham số hệ thống)
- Lưu các tham số cấu hình của hệ thống
- Chỉ có 1 bản ghi duy nhất
- Quản lý: độ tuổi, thời hạn thẻ, số sách mượn, tiền phạt...

### 2. **ReaderType** (Loại độc giả)  
- Phân loại độc giả: Sinh viên, Giảng viên, Học viên cao học...
- Mối quan hệ: 1 loại có nhiều độc giả

### 3. **Reader** (Độc giả)
- Thông tin chi tiết về độc giả
- Liên kết với ReaderType
- Tính năng: tự động tính tuổi, kiểm tra thẻ hết hạn, tính ngày hết hạn

## 🎯 Tính năng đặc biệt:

### Reader Model:
- **Properties tính toán**:
  - `age`: Tự động tính tuổi từ ngày sinh
  - `is_card_expired`: Kiểm tra thẻ hết hạn
  - `days_until_expiration`: Số ngày còn lại

- **Auto-save**: Tự động tính `expiration_date` dựa vào `card_validity_period`

### Parameter Model:
- **Singleton Pattern**: Chỉ cho phép 1 bản ghi duy nhất
- Không cho phép xóa trong Admin

## 🔧 Truy cập Admin Panel:

```bash
python manage.py createsuperuser
```

Sau đó truy cập: `http://localhost:8000/admin/`

### Quản lý trong Admin:
- ✅ Xem và chỉnh sửa tham số hệ thống
- ✅ Quản lý loại độc giả
- ✅ Quản lý độc giả với các filter, search
- ✅ Xem trạng thái thẻ, tuổi, nợ...
- ✅ Actions: Kích hoạt/vô hiệu hóa độc giả hàng loạt

## 📝 Ví dụ sử dụng trong code:

```python
from LibraryApp.models import Parameter, ReaderType, Reader

# Lấy tham số hệ thống
params = Parameter.objects.first()
print(f"Số sách tối đa: {params.max_borrowed_books}")

# Tạo loại độc giả
student_type = ReaderType.objects.create(
    reader_type_name='Sinh viên',
    description='Sinh viên đại học'
)

# Tạo độc giả
reader = Reader.objects.create(
    reader_name='Nguyễn Văn A',
    reader_type=student_type,
    date_of_birth=date(2002, 1, 1),
    email='nguyenvana@example.com',
    address='TP.HCM'
)

# Kiểm tra độc giả
print(f"Tuổi: {reader.age}")
print(f"Thẻ hết hạn: {reader.is_card_expired}")
print(f"Còn {reader.days_until_expiration} ngày")
```

## ⚠️ Lưu ý:

1. Đảm bảo đã cài `python-dateutil`:
   ```bash
   pip install python-dateutil
   ```

2. Database đang sử dụng PostgreSQL trên cloud (Neon)

3. Migrations được lưu trong `LibraryApp/migrations/`

4. Backup database trước khi thay đổi cấu trúc quan trọng
