"""
Script để tạo dữ liệu mẫu cho hệ thống quản lý thư viện
Chạy: python manage.py shell < seed_data.py
"""

from LibraryApp.models import (
    Parameter, ReaderType, Reader,
    Author, Category, BookTitle, AuthorDetail, Book, BookItem
)
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date

print("=== BẮT ĐẦU TẠO DỮ LIỆU MẪU ===\n")

# 1. Tạo Parameter (Tham số hệ thống)
print("1. Tạo tham số hệ thống...")
param, created = Parameter.objects.get_or_create(
    id=1,
    defaults={
        'max_age': 18,
        'min_age': 55,
        'card_validity_period': 6,
        'book_return_period': 8,
        'max_borrowed_books': 5,
        'max_borrow_days': 4,
        'fine_rate': 1000,
        'enable_receipt_amount_validation': True
    }
)
if created:
    print("   ✓ Đã tạo tham số hệ thống")
else:
    print("   → Tham số hệ thống đã tồn tại")

# 2. Tạo ReaderType (Loại độc giả)
print("\n2. Tạo loại độc giả...")
reader_types_data = [
    {'name': 'Sinh viên', 'desc': 'Sinh viên đang theo học tại trường'},
    {'name': 'Giảng viên', 'desc': 'Giảng viên giảng dạy tại trường'},
    {'name': 'Học viên cao học', 'desc': 'Học viên theo học chương trình sau đại học'},
    {'name': 'Độc giả bên ngoài', 'desc': 'Độc giả không thuộc trường'},
]

reader_types = {}
for rt_data in reader_types_data:
    rt, created = ReaderType.objects.get_or_create(
        reader_type_name=rt_data['name'],
        defaults={'description': rt_data['desc']}
    )
    reader_types[rt_data['name']] = rt
    if created:
        print(f"   ✓ Đã tạo loại độc giả: {rt_data['name']}")
    else:
        print(f"   → Loại độc giả đã tồn tại: {rt_data['name']}")

# 3. Tạo Reader (Độc giả mẫu)
print("\n3. Tạo độc giả mẫu...")
readers_data = [
    {
        'name': 'Nguyễn Văn An',
        'type': 'Sinh viên',
        'dob': date(2002, 3, 15),
        'email': 'nguyenvanan@example.com',
        'phone': '0901234567',
        'address': '123 Đường Nguyễn Văn Cừ, Q.5, TP.HCM'
    },
    {
        'name': 'Trần Thị Bình',
        'type': 'Giảng viên',
        'dob': date(1985, 7, 20),
        'email': 'tranthibinh@example.com',
        'phone': '0912345678',
        'address': '456 Đường Lý Thường Kiệt, Q.10, TP.HCM'
    },
    {
        'name': 'Lê Văn Cường',
        'type': 'Học viên cao học',
        'dob': date(1995, 11, 5),
        'email': 'levancuong@example.com',
        'phone': '0923456789',
        'address': '789 Đường Điện Biên Phủ, Q.3, TP.HCM'
    },
    {
        'name': 'Phạm Thị Dung',
        'type': 'Sinh viên',
        'dob': date(2003, 1, 10),
        'email': 'phamthidung@example.com',
        'phone': '0934567890',
        'address': '321 Đường Võ Văn Tần, Q.3, TP.HCM'
    },
    {
        'name': 'Hoàng Văn Ê',
        'type': 'Độc giả bên ngoài',
        'dob': date(1990, 5, 25),
        'email': 'hoangvane@example.com',
        'phone': '0945678901',
        'address': '654 Đường Cách Mạng Tháng 8, Q.Tân Bình, TP.HCM'
    },
]

for reader_data in readers_data:
    card_date = timezone.now()
    exp_date = card_date + relativedelta(months=param.card_validity_period)
    
    reader, created = Reader.objects.get_or_create(
        email=reader_data['email'],
        defaults={
            'reader_name': reader_data['name'],
            'reader_type': reader_types[reader_data['type']],
            'date_of_birth': reader_data['dob'],
            'address': reader_data['address'],
            'phone_number': reader_data['phone'],
            'card_creation_date': card_date,
            'expiration_date': exp_date,
            'total_debt': 0,
            'is_active': True
        }
    )
    if created:
        print(f"   ✓ Đã tạo độc giả: {reader_data['name']}")
    else:
        print(f"   → Độc giả đã tồn tại: {reader_data['name']}")

# 4. Tạo Category (Thể loại sách)
print("\n4. Tạo thể loại sách...")
categories_data = [
    {'name': 'Công nghệ thông tin', 'desc': 'Sách về lập trình, AI, ML...'},
    {'name': 'Văn học', 'desc': 'Tiểu thuyết, truyện ngắn, thơ...'},
    {'name': 'Khoa học', 'desc': 'Vật lý, Hóa học, Sinh học...'},
    {'name': 'Kinh tế', 'desc': 'Kinh tế học, Quản trị kinh doanh...'},
    {'name': 'Lịch sử', 'desc': 'Lịch sử Việt Nam và Thế giới'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        category_name=cat_data['name'],
        defaults={'description': cat_data['desc']}
    )
    categories[cat_data['name']] = cat
    if created:
        print(f"   ✓ Đã tạo thể loại: {cat_data['name']}")
    else:
        print(f"   → Thể loại đã tồn tại: {cat_data['name']}")

# 5. Tạo Author (Tác giả)
print("\n5. Tạo tác giả...")
authors_data = [
    'Nguyễn Nhật Ánh',
    'Tô Hoài',
    'Nam Cao',
    'Robert C. Martin',
    'Martin Fowler',
    'Eric Evans',
    'Yuval Noah Harari',
]

authors = {}
for author_name in authors_data:
    author, created = Author.objects.get_or_create(
        author_name=author_name
    )
    authors[author_name] = author
    if created:
        print(f"   ✓ Đã tạo tác giả: {author_name}")
    else:
        print(f"   → Tác giả đã tồn tại: {author_name}")

# 6. Tạo BookTitle (Tựa sách)
print("\n6. Tạo tựa sách...")
book_titles_data = [
    {
        'title': 'Clean Code',
        'category': 'Công nghệ thông tin',
        'authors': ['Robert C. Martin'],
        'desc': 'Cẩm nang viết code sạch và dễ bảo trì'
    },
    {
        'title': 'Refactoring',
        'category': 'Công nghệ thông tin',
        'authors': ['Martin Fowler'],
        'desc': 'Nghệ thuật cải thiện thiết kế code hiện có'
    },
    {
        'title': 'Domain-Driven Design',
        'category': 'Công nghệ thông tin',
        'authors': ['Eric Evans'],
        'desc': 'Thiết kế hướng miền trong phát triển phần mềm'
    },
    {
        'title': 'Sapiens',
        'category': 'Lịch sử',
        'authors': ['Yuval Noah Harari'],
        'desc': 'Lược sử loài người'
    },
    {
        'title': 'Dế Mèn phiêu lưu ký',
        'category': 'Văn học',
        'authors': ['Tô Hoài'],
        'desc': 'Truyện thiếu nhi nổi tiếng Việt Nam'
    },
    {
        'title': 'Chí Phèo',
        'category': 'Văn học',
        'authors': ['Nam Cao'],
        'desc': 'Truyện ngắn kinh điển văn học Việt Nam'
    },
]

book_titles = {}
for bt_data in book_titles_data:
    bt, created = BookTitle.objects.get_or_create(
        book_title=bt_data['title'],
        defaults={
            'category': categories[bt_data['category']],
            'description': bt_data['desc']
        }
    )
    book_titles[bt_data['title']] = bt
    
    # Thêm tác giả
    for author_name in bt_data['authors']:
        bt.authors.add(authors[author_name])
    
    if created:
        print(f"   ✓ Đã tạo tựa sách: {bt_data['title']}")
    else:
        print(f"   → Tựa sách đã tồn tại: {bt_data['title']}")

# 7. Tạo Book (Sách)
print("\n7. Tạo sách...")
books_data = [
    {
        'title': 'Clean Code',
        'publisher': 'Prentice Hall',
        'year': 2008,
        'price': 450000,
        'quantity': 10,
        'isbn': '978-0132350884'
    },
    {
        'title': 'Clean Code',
        'publisher': 'Prentice Hall',
        'year': 2020,
        'price': 500000,
        'quantity': 5,
        'isbn': '978-0132350885'
    },
    {
        'title': 'Refactoring',
        'publisher': 'Addison-Wesley',
        'year': 2018,
        'price': 550000,
        'quantity': 8,
        'isbn': '978-0134757599'
    },
    {
        'title': 'Sapiens',
        'publisher': 'NXB Trẻ',
        'year': 2019,
        'price': 200000,
        'quantity': 15,
        'isbn': '978-6041095823'
    },
    {
        'title': 'Dế Mèn phiêu lưu ký',
        'publisher': 'NXB Kim Đồng',
        'year': 2020,
        'price': 80000,
        'quantity': 20,
        'isbn': '978-6042123456'
    },
]

books = []
for book_data in books_data:
    book, created = Book.objects.get_or_create(
        book_title=book_titles[book_data['title']],
        publisher=book_data['publisher'],
        publish_year=book_data['year'],
        defaults={
            'quantity': book_data['quantity'],
            'remaining_quantity': book_data['quantity'],
            'unit_price': book_data['price'],
            'isbn': book_data.get('isbn', '')
        }
    )
    books.append(book)
    if created:
        print(f"   ✓ Đã tạo sách: {book_data['title']} ({book_data['year']})")
    else:
        print(f"   → Sách đã tồn tại: {book_data['title']} ({book_data['year']})")

# 8. Tạo BookItem (Cuốn sách cụ thể)
print("\n8. Tạo các cuốn sách...")
item_count = 0
for book in books:
    existing_items = BookItem.objects.filter(book=book).count()
    needed = book.quantity - existing_items
    
    if needed > 0:
        for i in range(needed):
            barcode = f"{book.id:04d}-{existing_items + i + 1:03d}"
            BookItem.objects.create(
                book=book,
                barcode=barcode,
                is_borrowed=False
            )
            item_count += 1

if item_count > 0:
    print(f"   ✓ Đã tạo {item_count} cuốn sách")
else:
    print(f"   → Tất cả các cuốn sách đã tồn tại")

print("\n=== HOÀN THÀNH TẠO DỮ LIỆU MẪU ===")
print(f"\nThống kê:")
print(f"  - Loại độc giả: {ReaderType.objects.count()}")
print(f"  - Độc giả: {Reader.objects.count()}")
print(f"  - Thể loại sách: {Category.objects.count()}")
print(f"  - Tác giả: {Author.objects.count()}")
print(f"  - Tựa sách: {BookTitle.objects.count()}")
print(f"  - Sách (phiên bản): {Book.objects.count()}")
print(f"  - Cuốn sách (vật lý): {BookItem.objects.count()}")

