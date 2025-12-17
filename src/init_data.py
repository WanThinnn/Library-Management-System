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
    BookTitle, Book, BookItem, Reader,
    UserGroup, Function, Permission, LibraryUser, BankAccount
)

def init_bank_account():
    """Khởi tạo tài khoản ngân hàng mặc định"""
    print("\n[*] Khoi tao tai khoan ngan hang:")
    bank, created = BankAccount.objects.get_or_create(
        id=1,
        defaults={
            'account_name': 'THU VIEN TRUONG',
            'account_no': '123456789',
            'bank_id': '970415',
            'template': 'print',
            'is_active': True
        }
    )
    if created:
        print(f"   [OK] {bank.account_name} - {bank.bank_id}")
    else:
        print(f"   [INFO] Tài khoản ngân hàng đã tồn tại")


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
        print("Tham số hệ thống đã tồn tại")
    
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
            print(f"{rt.reader_type_name}")
        else:
            print(f"{rt.reader_type_name} (đã tồn tại)")


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
            print(f"{c.category_name}")
        else:
            print(f"{c.category_name} (đã tồn tại)")


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
    
    print(f"Đã thêm {count} tác giả mới")
    print(f"Tổng: {Author.objects.count()} tác giả")


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
                    barcode=f"{book.id:04d}-{i+1:03d}",
                    defaults={
                        'is_borrowed': False,
                        'notes': ''
                    }
                )
                if item_created:
                    created_items += 1
            
            print(f"   [OK] {book_data['title']} ({book_data['quantity']} cuon)")
        else:
            print(f"   [INFO] {book_data['title']} (da ton tai)")
    
    print(f"\nTổng kết:")
    print(f"   - Đầu sách mới: {created_books}")
    print(f"   - BookItem mới: {created_items}")
    print(f"   - Tổng đầu sách: {Book.objects.count()}")
    print(f"   - Tổng số sách: {BookItem.objects.count()}")


def init_sample_readers():
    """Khởi tạo độc giả mẫu"""
    readers_data = [
        {
            'reader_name': 'Nguyễn Văn An',
            'date_of_birth': datetime(2000, 5, 15).date(),
            'email': 'nvan@example.com',
            'phone_number': '0901234567',
            'address': '123 Lê Lợi, Q.1, TP.HCM',
            'reader_type': 'Sinh viên'
        },
        {
            'reader_name': 'Trần Thị Bình',
            'date_of_birth': datetime(1999, 8, 20).date(),
            'email': 'ttbinh@example.com',
            'phone_number': '0912345678',
            'address': '456 Nguyễn Huệ, Q.1, TP.HCM',
            'reader_type': 'Sinh viên'
        },
        {
            'reader_name': 'Lê Văn Cường',
            'date_of_birth': datetime(1985, 3, 10).date(),
            'email': 'lvcuong@example.com',
            'phone_number': '0923456789',
            'address': '789 Trần Hưng Đạo, Q.5, TP.HCM',
            'reader_type': 'Giảng viên'
        },
        {
            'reader_name': 'Phạm Thị Dung',
            'date_of_birth': datetime(1990, 12, 25).date(),
            'email': 'ptdung@example.com',
            'phone_number': '0934567890',
            'address': '321 Võ Văn Tần, Q.3, TP.HCM',
            'reader_type': 'Cán bộ'
        },
        {
            'reader_name': 'Hoàng Văn Em',
            'date_of_birth': datetime(2001, 7, 5).date(),
            'email': 'hvem@example.com',
            'phone_number': '0945678901',
            'address': '654 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM',
            'reader_type': 'Sinh viên'
        },
    ]
    
    print("\n[*] Khoi tao doc gia mau:")
    created_count = 0
    card_expiry = datetime.now() + timedelta(days=180)  # 6 tháng
    
    for reader_data in readers_data:
        reader_type = ReaderType.objects.filter(
            reader_type_name=reader_data['reader_type']
        ).first()
        
        if not reader_type:
            continue
        
        reader, created = Reader.objects.get_or_create(
            email=reader_data['email'],
            defaults={
                'reader_name': reader_data['reader_name'],
                'date_of_birth': reader_data['date_of_birth'],
                'phone_number': reader_data['phone_number'],
                'address': reader_data['address'],
                'reader_type': reader_type,
                'card_creation_date': datetime.now(),
                'expiration_date': card_expiry,
                'total_debt': 0,
                'is_active': True
            }
        )
        
        if created:
            created_count += 1
            print(f"   [OK] {reader.reader_name} - {reader.email}")
        else:
            print(f"   [INFO] {reader.reader_name} (da ton tai)")
    
    print(f"\n   [INFO] Tong: {created_count} doc gia moi / {Reader.objects.count()} tong")


def create_superuser():
    """Tạo tài khoản superuser nếu chưa có"""
    print("\n[*] Kiem tra tai khoan superuser:")
    
    if User.objects.filter(is_superuser=True).exists():
        admin = User.objects.filter(is_superuser=True).first()
        print(f"Đã có superuser: {admin.username}")
        return admin
    
    try:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@library.local',
            password='Admin1234!@#$',
            first_name='Admin',
            last_name='System'
        )
        print(f"Đã tạo superuser: admin / Admin1234!@#$")
        return admin
    except Exception as e:
        print(f"Lỗi tạo superuser: {e}")
        return None


def init_user_groups():
    """Khởi tạo nhóm người dùng (User Groups) - Chỉ 2 nhóm: Quản lý và Thủ thư"""
    user_groups = [
        {
            'name': 'Quản lý',
            'description': 'Quản lý thư viện, có toàn quyền với tất cả chức năng'
        },
        {
            'name': 'Thủ thư',
            'description': 'Nhân viên thư viện, xử lý nghiệp vụ hàng ngày'
        }
    ]
    
    print("\n[*] Khoi tao nhom nguoi dung:")
    created_count = 0
    
    for group_data in user_groups:
        group, created = UserGroup.objects.get_or_create(
            user_group_name=group_data['name'],
            defaults={'description': group_data['description']}
        )
        
        if created:
            created_count += 1
            print(f"   [OK] {group.user_group_name}")
        else:
            print(f"   [INFO] {group.user_group_name} (đã tồn tại)")
    
    print(f"Tổng: {created_count} nhóm mới / {UserGroup.objects.count()} nhóm")


def init_functions():
    """Khởi tạo các chức năng/màn hình trong hệ thống"""
    functions = [
        # Quản lý độc giả
        {'name': 'Quản lý độc giả', 'screen': 'Danh sách độc giả', 'url': '/readers/'},
        {'name': 'Lập thẻ độc giả', 'screen': 'Tạo thẻ độc giả mới', 'url': '/readers/create/'},
        
        # Quản lý sách
        {'name': 'Tra cứu sách', 'screen': 'Tìm kiếm sách', 'url': '/books/search/'},
        {'name': 'Lập phiếu nhập sách', 'screen': 'Nhập sách vào kho', 'url': '/books/import/'},
        {'name': 'Quản lý kho sách', 'screen': 'Danh sách sách trong kho', 'url': '/books/'},
        
        # Mượn/Trả sách
        {'name': 'Lập phiếu mượn sách', 'screen': 'Tạo phiếu mượn', 'url': '/borrow/'},
        {'name': 'Lập phiếu trả sách', 'screen': 'Xử lý trả sách', 'url': '/return/'},
        {'name': 'Quản lý mượn/trả', 'screen': 'Danh sách phiếu mượn/trả', 'url': '/borrow/list/'},
        
        # Thu tiền
        {'name': 'Lập phiếu thu tiền phạt', 'screen': 'Thu tiền phạt trả trễ', 'url': '/receipts/create/'},
        {'name': 'Quản lý phiếu thu', 'screen': 'Danh sách phiếu thu', 'url': '/receipts/'},
        
        # Báo cáo
        {'name': 'Báo cáo mượn sách theo thể loại', 'screen': 'Thống kê theo thể loại', 'url': '/reports/borrow-by-category/'},
        {'name': 'Báo cáo sách trả trễ', 'screen': 'Danh sách sách trả trễ', 'url': '/reports/overdue-books/'},
        
        # Quản trị hệ thống
        {'name': 'Quản lý người dùng', 'screen': 'Danh sách thủ thư', 'url': '/users/'},
        {'name': 'Thay đổi quy định', 'screen': 'Cập nhật tham số hệ thống', 'url': '/settings/'},
    ]
    
    print("\n[*] Khoi tao chuc nang he thong:")
    created_count = 0
    
    for func_data in functions:
        func, created = Function.objects.get_or_create(
            function_name=func_data['name'],
            defaults={
                'screen_name': func_data['screen'],
                'url_pattern': func_data['url'],
                'description': f"Chức năng {func_data['name']}"
            }
        )
        
        if created:
            created_count += 1
            print(f"   [OK] {func.function_name}")
        else:
            print(f"   [INFO] {func.function_name} (đã tồn tại)")
    
    print(f"Tổng: {created_count} chức năng mới / {Function.objects.count()} chức năng")


def init_permissions():
    """Phân quyền cho từng nhóm người dùng - Quản lý và Thủ thư"""
    quan_ly = UserGroup.objects.filter(user_group_name='Quản lý').first()
    thu_thu = UserGroup.objects.filter(user_group_name='Thủ thư').first()
    
    permissions_config = {
        'Quản lý': {
            # Toàn quyền tất cả chức năng
            'all': {'view': True, 'add': True, 'edit': True, 'delete': True}
        },
        'Thủ thư': {
            # Xử lý nghiệp vụ hàng ngày, không có quyền xóa và thay đổi quy định
            'Quản lý độc giả': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Lập thẻ độc giả': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Tra cứu sách': {'view': True, 'add': False, 'edit': False, 'delete': False},
            'Lập phiếu nhập sách': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Quản lý kho sách': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Lập phiếu mượn sách': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Lập phiếu trả sách': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Quản lý mượn/trả': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Lập phiếu thu tiền phạt': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Quản lý phiếu thu': {'view': True, 'add': True, 'edit': True, 'delete': False},
            'Báo cáo mượn sách theo thể loại': {'view': True, 'add': False, 'edit': False, 'delete': False},
            'Báo cáo sách trả trễ': {'view': True, 'add': False, 'edit': False, 'delete': False},
            # Thủ thư KHÔNG có quyền quản lý người dùng và thay đổi quy định
        }
    }
    
    print("\n[*] Phan quyen cho cac nhom nguoi dung:")
    created_count = 0
    
    # Quản lý - toàn quyền tất cả chức năng
    if quan_ly:
        print(f"\n   Nhóm: {quan_ly.user_group_name}")
        for func in Function.objects.all():
            perm, created = Permission.objects.get_or_create(
                user_group=quan_ly,
                function=func,
                defaults={
                    'can_view': True,
                    'can_add': True,
                    'can_edit': True,
                    'can_delete': True
                }
            )
            if created:
                created_count += 1
                print(f"      [OK] {func.function_name} - Toàn quyền")
    
    # Thủ thư - quyền hạn chế
    if thu_thu:
        print(f"\n   Nhóm: {thu_thu.user_group_name}")
        for func_name, perm_data in permissions_config['Thủ thư'].items():
            func = Function.objects.filter(function_name=func_name).first()
            if not func:
                continue
            
            perm, created = Permission.objects.get_or_create(
                user_group=thu_thu,
                function=func,
                defaults={
                    'can_view': perm_data['view'],
                    'can_add': perm_data['add'],
                    'can_edit': perm_data['edit'],
                    'can_delete': perm_data['delete']
                }
            )
            
            if created:
                created_count += 1
                perms_str = []
                if perm_data['view']: perms_str.append('Xem')
                if perm_data['add']: perms_str.append('Thêm')
                if perm_data['edit']: perms_str.append('Sửa')
                if perm_data['delete']: perms_str.append('Xóa')
                print(f"      [OK] {func.function_name} - {', '.join(perms_str)}")
    
    print(f"\nTổng: {created_count} quyền mới / {Permission.objects.count()} quyền")


def init_library_users():
    """Tạo tài khoản thủ thư mẫu - Quản lý và Thủ thư"""
    # Lấy superuser đã tạo
    admin_user = User.objects.filter(username='admin').first()
    quan_ly_group = UserGroup.objects.filter(user_group_name='Quản lý').first()
    
    # Tạo LibraryUser cho admin (Quản lý)
    if admin_user and quan_ly_group:
        lib_admin, created = LibraryUser.objects.get_or_create(
            user=admin_user,
            defaults={
                'full_name': 'Nguyễn Văn Quản Lý',
                'date_of_birth': datetime(1985, 1, 15).date(),
                'position': 'Quản lý thư viện',
                'user_group': quan_ly_group,
                'phone_number': '0900000000',
                'email': 'admin@library.local',
                'address': 'Thư viện trường',
                'is_active': True
            }
        )
        
        if created:
            print("\n[*] Tao tai khoan LibraryUser:")
            print(f"   [OK] {lib_admin.full_name} - {lib_admin.position}")
            print(f"        Username: admin / Password: Admin1234!@#$")
    
    # Tạo thêm thủ thư mẫu
    thu_thu_group = UserGroup.objects.filter(user_group_name='Thủ thư').first()
    
    if thu_thu_group:
        # Tạo Django User
        user, created = User.objects.get_or_create(
            username='thuthu01',
            defaults={
                'email': 'thuthu01@library.local',
                'first_name': 'Thủ',
                'last_name': 'Thư 01',
                'is_staff': True
            }
        )
        
        if created:
            user.set_password('Thuthu1234!@#$')
            user.save()
        
        # Tạo LibraryUser
        lib_user, created = LibraryUser.objects.get_or_create(
            user=user,
            defaults={
                'full_name': 'Trần Thị Thu Thư',
                'date_of_birth': datetime(1995, 5, 20).date(),
                'position': 'Thủ thư',
                'user_group': thu_thu_group,
                'phone_number': '0911111111',
                'email': 'thuthu01@library.local',
                'address': 'TP.HCM',
                'is_active': True
            }
        )
        
        if created:
            print(f"   [OK] {lib_user.full_name} - {lib_user.position}")
            print(f"        Username: thuthu01 / Password: Thuthu1234!@#$")


def main():
    print("="*70)
    print("KHOI TAO DU LIEU DAY DU - HE THONG QUAN LY THU VIEN")
    print("="*70)
    
    try:
        # 0. Tạo superuser
        create_superuser()
        
        # 1. Tham số hệ thống (QĐ1-QĐ6)
        init_parameters()
        init_bank_account()
        
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
        
        # 7. Nhóm người dùng (User Groups)
        init_user_groups()
        
        # 8. Chức năng hệ thống (Functions)
        init_functions()
        
        # 9. Phân quyền (Permissions)
        init_permissions()
        
        # 10. Tài khoản thủ thư (LibraryUsers)
        init_library_users()
        
        print("\n" + "="*70)
        print("HOÀN TẤT! Hệ thống đã sẵn sàng với dữ liệu đầy đủ.")
        print("="*70)
        print("\nThông tin đăng nhập:")
        print("   Quản lý:")
        print("      Username: admin")
        print("      Password: Admin1234!@#$")
        print("      Quyền: Toàn quyền tất cả chức năng")
        print("\n   Thủ thư:")
        print("      Username: thuthu01")
        print("      Password: Thuthu1234!@#$")
        print("      Quyền: Xử lý nghiệp vụ (không xóa, không thay đổi quy định)")
        print("\nBước tiếp theo:")
        print("   1. Truy cập: https://library.cyberfortress.local/ hoặc http://localhost:8000")
        print("   2. Đăng nhập với tài khoản admin hoặc thuthu01")
        print("   3. Thử nghiệm các chức năng:")
        print("      - Quản lý độc giả")
        print("      - Nhập sách")
        print("      - Lập phiếu mượn")
        print("      - Lập phiếu trả")
        print("      - Lập phiếu thu tiền phạt")
        print("      - Báo cáo thống kê")
        print("\nDữ liệu đã tạo:")
        print(f"   - Tham số hệ thống: 1")
        print(f"   - Loại độc giả: {ReaderType.objects.count()}")
        print(f"   - Thể loại sách: {Category.objects.count()}")
        print(f"   - Tác giả: {Author.objects.count()}")
        print(f"   - Đầu sách: {Book.objects.count()}")
        print(f"   - Số sách vật lý: {BookItem.objects.count()}")
        print(f"   - Độc giả: {Reader.objects.count()}")
        print(f"   - Tài khoản admin: {User.objects.filter(is_superuser=True).count()}")
        print(f"   - Nhóm người dùng: {UserGroup.objects.count()} (Quản lý + Thủ thư)")
        print(f"   - Chức năng hệ thống: {Function.objects.count()}")
        print(f"   - Phân quyền: {Permission.objects.count()}")
        print(f"   - Thủ thư: {LibraryUser.objects.count()}")
        print()
        
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
