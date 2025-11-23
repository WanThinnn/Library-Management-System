"""
Script khởi tạo dữ liệu ban đầu đầy đủ cho hệ thống thư viện
Bao gồm: Parameters, ReaderTypes, Categories, Authors, Books, Readers, BookItems
Chạy: python init_data.py
Hoặc trong Docker: docker compose exec web python /app/init_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')
django.setup()

from django.contrib.auth.models import User
from LibraryApp.models import (
    Parameter, ReaderType, Category, Author, AuthorDetail,
    BookTitle, Book, BookItem, Reader
)

def init_parameters():
    """Khởi tạo tham số hệ thống đầy đủ (QĐ1-QĐ6)"""
    param, created = Parameter.objects.get_or_create(
        id=1,
        defaults={
            # QĐ1: Quy định về độc giả
            'min_age': 18,
            'max_age': 55,
            'card_validity_period': 6,  # tháng
            
            # QĐ2: Quy định về sách
            'book_return_period': 8,  # năm (chỉ nhận sách xuất bản trong 8 năm gần đây)
            
            # QĐ4: Quy định về mượn sách
            'max_borrowed_books': 5,
            'max_borrow_days': 30,  # ngày
            
            # QĐ5: Quy định về tiền phạt
            'fine_rate': 1000,  # 1000đ/ngày trả trễ
            
            # QĐ6: Quy định về thu tiền
            'enable_receipt_amount_validation': True,
        }
    )
    
    if created:
        print("[OK] Da tao tham so he thong mac dinh:")
        print(f"   - Độ tuổi độc giả: {param.min_age} - {param.max_age} tuổi")
        print(f"   - Thời hạn thẻ: {param.card_validity_period} tháng")
        print(f"   - Sách xuất bản trong: {param.book_return_period} năm gần đây")
        print(f"   - Số sách mượn tối đa: {param.max_borrowed_books} quyển")
        print(f"   - Số ngày mượn tối đa: {param.max_borrow_days} ngày")
        print(f"   - Tiền phạt trễ hạn: {param.fine_rate:,}đ/ngày")
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
    
    print("\n[*] Khoi tao loai doc gia:")
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
    
    print("\n[*] Khoi tao the loai sach:")
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
    """Khởi tạo tác giả mẫu"""
    authors = [
        # Tác giả Việt Nam
        'Nguyễn Nhật Ánh',
        'Tô Hoài',
        'Nam Cao',
        'Nguyễn Du',
        'Xuân Diệu',
        'Ngô Tất Tố',
        'Vũ Trọng Phụng',
        'Hồ Chí Minh',
        
        # Tác giả nước ngoài - IT
        'Robert C. Martin',
        'Martin Fowler',
        'Eric Evans',
        'Andrew Hunt',
        'David Thomas',
        'Gang of Four',
        'Michael Feathers',
        'Kent Beck',
        
        # Tác giả nước ngoài - Kỹ năng sống
        'Dale Carnegie',
        'Stephen Covey',
        'Napoleon Hill',
        'Robin Sharma',
        'Haruki Murakami',
        'Paulo Coelho',
    ]
    
    print("\n[*] Khoi tao tac gia mau:")
    count = 0
    for author_name in authors:
        a, created = Author.objects.get_or_create(
            author_name=author_name
        )
        if created:
            count += 1
    
    print(f"   ✅ Đã thêm {count} tác giả mới")
    print(f"   ℹ️  Tổng: {Author.objects.count()} tác giả")


def init_books():
    """Khởi tạo sách mẫu với BookTitle, Book và BookItem"""
    current_year = datetime.now().year
    
    books_data = [
        # IT Books
        {
            'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
            'author': 'Robert C. Martin',
            'category': 'Công nghệ thông tin',
            'publisher': 'Prentice Hall',
            'publish_year': 2008,
            'price': 450000,
            'quantity': 3
        },
        {
            'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
            'author': 'Gang of Four',
            'category': 'Công nghệ thông tin',
            'publisher': 'Addison-Wesley',
            'publish_year': 1994,
            'price': 550000,
            'quantity': 2
        },
        {
            'title': 'Refactoring: Improving the Design of Existing Code',
            'author': 'Martin Fowler',
            'category': 'Công nghệ thông tin',
            'publisher': 'Addison-Wesley',
            'publish_year': 2018,
            'price': 480000,
            'quantity': 3
        },
        {
            'title': 'The Pragmatic Programmer',
            'author': 'Andrew Hunt',
            'category': 'Công nghệ thông tin',
            'publisher': 'Addison-Wesley',
            'publish_year': 2019,
            'price': 420000,
            'quantity': 4
        },
        
        # Vietnamese Literature
        {
            'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
            'author': 'Nguyễn Nhật Ánh',
            'category': 'Văn học',
            'publisher': 'Trẻ',
            'publish_year': 2010,
            'price': 120000,
            'quantity': 5
        },
        {
            'title': 'Dế Mèn Phiêu Lưu Ký',
            'author': 'Tô Hoài',
            'category': 'Văn học',
            'publisher': 'Kim Đồng',
            'publish_year': 1941,
            'price': 80000,
            'quantity': 4
        },
        {
            'title': 'Chí Phèo',
            'author': 'Nam Cao',
            'category': 'Văn học',
            'publisher': 'Văn học',
            'publish_year': 1941,
            'price': 65000,
            'quantity': 3
        },
        
        # Self-help books
        {
            'title': 'Đắc Nhân Tâm',
            'author': 'Dale Carnegie',
            'category': 'Kỹ năng sống',
            'publisher': 'First News',
            'publish_year': 2020,
            'price': 95000,
            'quantity': 6
        },
        {
            'title': '7 Thói Quen Của Người Thành Đạt',
            'author': 'Stephen Covey',
            'category': 'Kỹ năng sống',
            'publisher': 'First News',
            'publish_year': 2019,
            'price': 110000,
            'quantity': 4
        },
        {
            'title': 'Nghĩ Giàu Làm Giàu',
            'author': 'Napoleon Hill',
            'category': 'Kỹ năng sống',
            'publisher': 'Trẻ',
            'publish_year': 2021,
            'price': 98000,
            'quantity': 5
        },
        
        # Science
        {
            'title': 'Sapiens: Lược Sử Loài Người',
            'author': 'Haruki Murakami',
            'category': 'Khoa học',
            'publisher': 'Thế Giới',
            'publish_year': 2018,
            'price': 180000,
            'quantity': 3
        },
    ]
    
    print("\n[*] Khoi tao sach mau:")
    created_books = 0
    created_items = 0
    
    for book_data in books_data:
        # Get author
        author = Author.objects.filter(author_name=book_data['author']).first()
        if not author:
            author = Author.objects.create(author_name=book_data['author'])
        
        # Get category
        category = Category.objects.filter(category_name=book_data['category']).first()
        if not category:
            category = Category.objects.create(
                category_name=book_data['category'],
                description=f"Thể loại {book_data['category']}"
            )
        
        # Create BookTitle
        book_title, title_created = BookTitle.objects.get_or_create(
            book_title=book_data['title'],
            defaults={
                'category': category,
                'description': f"Mô tả sách {book_data['title']}"
            }
        )
        
        # Create AuthorDetail (link author to book_title)
        author_detail, _ = AuthorDetail.objects.get_or_create(
            author=author,
            book_title=book_title
        )
        
        # Create Book
        book, book_created = Book.objects.get_or_create(
            book_title=book_title,
            defaults={
                'publisher': book_data['publisher'],
                'publish_year': book_data['publish_year'],
                'unit_price': Decimal(str(book_data['price'])),
                'quantity': book_data['quantity'],
                'remaining_quantity': book_data['quantity']
            }
        )
        
        if book_created:
            created_books += 1
            
            # Create BookItems
            for i in range(book_data['quantity']):
                item, item_created = BookItem.objects.get_or_create(
                    book=book,
                    item_code=f"{book.id:04d}-{i+1:03d}",
                    defaults={
                        'status': 'available',
                        'condition': 'good'
                    }
                )
                if item_created:
                    created_items += 1
            
            print(f"   [OK] {book_data['title']} ({book_data['quantity']} cuon)")
        else:
            print(f"   [INFO] {book_data['title']} (da ton tai)")
    
    print(f"\n   📊 Tổng kết:")
    print(f"   - Đầu sách mới: {created_books}")
    print(f"   - BookItem mới: {created_items}")
    print(f"   - Tổng đầu sách: {Book.objects.count()}")
    print(f"   - Tổng số sách: {BookItem.objects.count()}")


def init_sample_readers():
    """Khởi tạo độc giả mẫu"""
    readers_data = [
        {
            'full_name': 'Nguyễn Văn An',
            'date_of_birth': datetime(2000, 5, 15).date(),
            'email': 'nvan@example.com',
            'phone': '0901234567',
            'address': '123 Lê Lợi, Q.1, TP.HCM',
            'reader_type': 'Sinh viên'
        },
        {
            'full_name': 'Trần Thị Bình',
            'date_of_birth': datetime(1999, 8, 20).date(),
            'email': 'ttbinh@example.com',
            'phone': '0912345678',
            'address': '456 Nguyễn Huệ, Q.1, TP.HCM',
            'reader_type': 'Sinh viên'
        },
        {
            'full_name': 'Lê Văn Cường',
            'date_of_birth': datetime(1985, 3, 10).date(),
            'email': 'lvcuong@example.com',
            'phone': '0923456789',
            'address': '789 Trần Hưng Đạo, Q.5, TP.HCM',
            'reader_type': 'Giảng viên'
        },
        {
            'full_name': 'Phạm Thị Dung',
            'date_of_birth': datetime(1990, 12, 25).date(),
            'email': 'ptdung@example.com',
            'phone': '0934567890',
            'address': '321 Võ Văn Tần, Q.3, TP.HCM',
            'reader_type': 'Cán bộ'
        },
        {
            'full_name': 'Hoàng Văn Em',
            'date_of_birth': datetime(2001, 7, 5).date(),
            'email': 'hvem@example.com',
            'phone': '0945678901',
            'address': '654 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM',
            'reader_type': 'Sinh viên'
        },
    ]
    
    print("\n[*] Khoi tao doc gia mau:")
    created_count = 0
    card_expiry = datetime.now().date() + timedelta(days=180)  # 6 tháng
    
    for reader_data in readers_data:
        reader_type = ReaderType.objects.filter(
            reader_type_name=reader_data['reader_type']
        ).first()
        
        if not reader_type:
            continue
        
        reader, created = Reader.objects.get_or_create(
            email=reader_data['email'],
            defaults={
                'full_name': reader_data['full_name'],
                'date_of_birth': reader_data['date_of_birth'],
                'phone': reader_data['phone'],
                'address': reader_data['address'],
                'reader_type': reader_type,
                'card_number': f"DG{datetime.now().year}{Reader.objects.count() + 1:05d}",
                'card_issue_date': datetime.now().date(),
                'card_expiry_date': card_expiry,
                'status': 'active'
            }
        )
        
        if created:
            created_count += 1
            print(f"   ✅ {reader.full_name} - {reader.card_number}")
        else:
            print(f"   ℹ️  {reader.full_name} (đã tồn tại)")
    
    print(f"\n   📊 Tổng: {created_count} độc giả mới / {Reader.objects.count()} tổng")


def create_superuser():
    """Tạo tài khoản superuser nếu chưa có"""
    print("\n[*] Kiem tra tai khoan superuser:")
    
    if User.objects.filter(is_superuser=True).exists():
        admin = User.objects.filter(is_superuser=True).first()
        print(f"   ℹ️  Đã có superuser: {admin.username}")
        return admin
    
    try:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@library.local',
            password='admin123',
            first_name='Admin',
            last_name='System'
        )
        print(f"   ✅ Đã tạo superuser: admin / admin123")
        return admin
    except Exception as e:
        print(f"   ⚠️  Lỗi tạo superuser: {e}")
        return None


def main():
    print("="*70)
    print("KHOI TAO DU LIEU DAY DU - HE THONG QUAN LY THU VIEN")
    print("="*70)
    
    try:
        # 0. Tạo superuser
        create_superuser()
        
        # 1. Tham số hệ thống (QĐ1-QĐ6)
        init_parameters()
        
        # 2. Loại độc giả
        init_reader_types()
        
        # 3. Thể loại sách
        init_categories()
        
        # 4. Tác giả
        init_authors()
        
        # 5. Sách mẫu (BookTitle, Book, BookItem)
        init_books()
        
        # 6. Độc giả mẫu
        init_sample_readers()
        
        print("\n" + "="*70)
        print("✅ HOÀN TẤT! Hệ thống đã sẵn sàng với dữ liệu đầy đủ.")
        print("="*70)
        print("\n📌 Thông tin đăng nhập:")
        print("   👤 Username: admin")
        print("   🔑 Password: admin123")
        print("\n📌 Bước tiếp theo:")
        print("   1. Truy cập: https://library.cyberfortress.local/")
        print("   2. Đăng nhập với tài khoản admin")
        print("   3. Thử nghiệm các chức năng:")
        print("      - Quản lý độc giả")
        print("      - Nhập sách")
        print("      - Lập phiếu mượn")
        print("      - Lập phiếu trả")
        print("      - Lập phiếu thu tiền phạt")
        print("      - Báo cáo thống kê")
        print("\n📊 Dữ liệu đã tạo:")
        print(f"   - Tham số hệ thống: 1")
        print(f"   - Loại độc giả: {ReaderType.objects.count()}")
        print(f"   - Thể loại sách: {Category.objects.count()}")
        print(f"   - Tác giả: {Author.objects.count()}")
        print(f"   - Đầu sách: {Book.objects.count()}")
        print(f"   - Số sách vật lý: {BookItem.objects.count()}")
        print(f"   - Độc giả: {Reader.objects.count()}")
        print(f"   - Tài khoản admin: {User.objects.filter(is_superuser=True).count()}")
        print()
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
