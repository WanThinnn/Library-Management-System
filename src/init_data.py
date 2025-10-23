"""
Script khởi tạo dữ liệu ban đầu cho hệ thống thư viện
Chạy: python manage.py shell < init_data.py
Hoặc: python init_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')
django.setup()

from LibraryApp.models import Parameter, ReaderType, Category, Author

def init_parameters():
    """Khởi tạo tham số hệ thống (QĐ1, QĐ2, QĐ4, QĐ5, QĐ6)"""
    param, created = Parameter.objects.get_or_create(
        id=1,
        defaults={
            # QĐ1: Quy định về độc giả
            'min_age': 18,
            'max_age': 55,
            'card_validity_period': 6,  # tháng
            
            # QĐ2: Quy định về sách (sẽ thêm max_book_age sau)
            'book_return_period': 30,  # ngày (tạm thời)
            
            # QĐ4: Quy định về mượn sách
            'max_borrowed_books': 5,
            'max_borrow_days': 30,  # 1 tháng
            
            # QĐ5: Quy định về tiền phạt
            'fine_rate': 1000,  # 1000đ/ngày
            
            # QĐ6: Quy định về thu tiền
            'enable_receipt_amount_validation': True,
        }
    )
    
    if created:
        print("✅ Đã tạo tham số hệ thống mặc định:")
        print(f"   - Tuổi độc giả: {param.min_age} - {param.max_age} tuổi")
        print(f"   - Thời hạn thẻ: {param.card_validity_period} tháng")
        print(f"   - Số sách mượn tối đa: {param.max_borrowed_books} quyển")
        print(f"   - Số ngày mượn tối đa: {param.max_borrow_days} ngày")
        print(f"   - Tiền phạt: {param.fine_rate:,}đ/ngày")
    else:
        print("ℹ️  Tham số hệ thống đã tồn tại")
    
    return param


def init_reader_types():
    """Khởi tạo loại độc giả (QĐ1)"""
    reader_types = [
        {
            'reader_type_name': 'Sinh viên',
            'description': 'Sinh viên đang học tại trường'
        },
        {
            'reader_type_name': 'Giảng viên',
            'description': 'Giảng viên, giáo viên của trường'
        },
        {
            'reader_type_name': 'Cán bộ',
            'description': 'Cán bộ, nhân viên của trường'
        },
        {
            'reader_type_name': 'Khách',
            'description': 'Độc giả bên ngoài'
        }
    ]
    
    print("\n📋 Khởi tạo loại độc giả:")
    for rt_data in reader_types:
        rt, created = ReaderType.objects.get_or_create(
            reader_type_name=rt_data['reader_type_name'],
            defaults={'description': rt_data['description']}
        )
        if created:
            print(f"   ✅ {rt.reader_type_name}")
        else:
            print(f"   ℹ️  {rt.reader_type_name} (đã tồn tại)")


def init_categories():
    """Khởi tạo thể loại sách (QĐ2)"""
    categories = [
        {'name': 'Công nghệ thông tin', 'desc': 'Sách về lập trình, mạng, CSDL, AI...'},
        {'name': 'Văn học', 'desc': 'Tiểu thuyết, thơ, truyện ngắn...'},
        {'name': 'Khoa học', 'desc': 'Toán, Lý, Hóa, Sinh...'},
        {'name': 'Kinh tế', 'desc': 'Quản trị, Marketing, Tài chính...'},
        {'name': 'Kỹ năng sống', 'desc': 'Phát triển bản thân, giao tiếp...'},
        {'name': 'Lịch sử', 'desc': 'Lịch sử Việt Nam và thế giới'},
        {'name': 'Ngoại ngữ', 'desc': 'Tiếng Anh, Nhật, Hàn, Trung...'},
        {'name': 'Khác', 'desc': 'Các thể loại khác'}
    ]
    
    print("\n📚 Khởi tạo thể loại sách:")
    for cat in categories:
        c, created = Category.objects.get_or_create(
            category_name=cat['name'],
            defaults={'description': cat['desc']}
        )
        if created:
            print(f"   ✅ {c.category_name}")
        else:
            print(f"   ℹ️  {c.category_name} (đã tồn tại)")


def init_authors():
    """Khởi tạo một số tác giả mẫu"""
    authors = [
        'Nguyễn Nhật Ánh',
        'Tô Hoài',
        'Nam Cao',
        'Nguyễn Du',
        'Xuân Diệu',
        'Robert C. Martin',
        'Martin Fowler',
        'Eric Evans',
        'Andrew Hunt',
        'Dale Carnegie'
    ]
    
    print("\n✍️  Khởi tạo tác giả mẫu:")
    count = 0
    for author_name in authors:
        a, created = Author.objects.get_or_create(
            author_name=author_name
        )
        if created:
            count += 1
    
    print(f"   ✅ Đã thêm {count} tác giả mới")
    print(f"   ℹ️  Tổng: {Author.objects.count()} tác giả")


def main():
    print("="*60)
    print("🚀 KHỞI TẠO DỮ LIỆU HỆ THỐNG THƯ VIỆN")
    print("="*60)
    
    try:
        # 1. Tham số hệ thống (bắt buộc)
        init_parameters()
        
        # 2. Loại độc giả (bắt buộc)
        init_reader_types()
        
        # 3. Thể loại sách (bắt buộc)
        init_categories()
        
        # 4. Tác giả (optional)
        init_authors()
        
        print("\n" + "="*60)
        print("✅ HOÀN TẤT! Hệ thống đã sẵn sàng sử dụng.")
        print("="*60)
        print("\n📌 Bước tiếp theo:")
        print("   1. Truy cập: http://127.0.0.1:8080/login/")
        print("   2. Đăng nhập với tài khoản superuser")
        print("   3. Lập thẻ độc giả: http://127.0.0.1:8080/reader/create/")
        print()
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
