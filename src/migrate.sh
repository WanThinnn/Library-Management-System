#!/bin/bash
# Script để tạo và chạy migrations

echo "=== Tạo migrations cho các models mới ==="
python manage.py makemigrations LibraryApp

echo ""
echo "=== Chạy migrations ==="
python manage.py migrate

echo ""
echo "=== Hoàn thành! ==="
