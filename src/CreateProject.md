# Hướng dẫn Tạo Project Django: Library-Management-System

## 1. Tạo môi trường ảo với Conda
Mở **Anaconda Prompt** hoặc **PowerShell** 

```bash
# Tạo môi trường ảo tên "library_env" với Python 3.10
conda create -n library_env python=3.10

# Kích hoạt môi trường
conda activate library_env
````

> Nếu dùng Git Bash, cần thêm dòng sau vào `~/.bashrc` để `conda activate` hoạt động:
>
> ```bash
> source /c/ProgramData/miniconda3/etc/profile.d/conda.sh
> ```

---

## 2. Cài đặt Django

```bash
pip install django
```

---

## 3. Tạo project Django (không chạy phần này)

Trong thư mục `Library-Management-System`, chạy:

```bash
django-admin startproject LibraryManagementSystem .
```

Cấu trúc sau khi tạo:

```
Library-Management-System/
│   manage.py
│
├── LibraryManagementSystem/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
```

---

## 4. Chạy thử server

```bash
python manage.py runserver
```

Mở trình duyệt tại `http://127.0.0.1:8000/`.
Nếu thấy trang chúc mừng → tạo project thành công ✅

---

## 5. Tạo app `LibraryApp` (không chạy phần)

```bash
python manage.py startapp LibraryApp 
```

Sau khi tạo, cấu trúc sẽ có thêm:

```
LibraryApp/
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

Rồi thêm `"LibraryApp"` vào `INSTALLED_APPS` trong `LibraryManagementSystem/settings.py`.

---

## 6. Kết nối PostgreSQL

Cài driver:

```bash
pip install psycopg2-binary
```

Trong `settings.py`, chỉnh phần `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 7. Tạo và áp dụng migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 8. Tạo tài khoản admin

```bash
python manage.py createsuperuser
```

---

## 9. Truy cập Django Admin

Chạy lại server:

```bash
python manage.py runserver
```

Truy cập `http://127.0.0.1:8000/admin/` → đăng nhập bằng tài khoản vừa tạo.

---

🎉 Như vậy bạn đã khởi tạo xong project **Library-Management-System** bằng Django trong môi trường Conda Python 3.10.

```

---

Bạn có muốn mình tạo sẵn **file `CreateProject.md`** trong project để bạn tải về không?
```
