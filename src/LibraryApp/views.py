from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import BankAccount, Reader, ReaderType, Parameter, BookTitle, Author, BookImportReceipt, BookImportDetail, Book, AuthorDetail, BookItem, BorrowReturnReceipt, Receipt, Category, UserGroup, Function, Permission
from .forms import ReaderForm, LibraryLoginForm, BookImportForm, BookSearchForm, BorrowBookForm, ReturnBookForm, ReceiptForm, ParameterForm, BookEditForm, ReaderTypeForm, UserGroupForm, FunctionForm
from .decorators import manager_required, staff_required, permission_required


def home_view(request):
    """Trang chủ hệ thống với dashboard statistics"""
    context = {}
    
    if request.user.is_authenticated:
        # Đếm tổng số độc giả
        context['total_readers'] = Reader.objects.filter(is_active=True).count()
        
        # Đếm tổng số đầu sách (BookTitle)
        context['total_books'] = BookTitle.objects.count()
        
        # Đếm số phiếu mượn đang hoạt động (chưa trả)
        context['active_borrows'] = BorrowReturnReceipt.objects.filter(
            return_date__isnull=True
        ).count()
        
        # Đếm số sách quá hạn
        from datetime import date
        context['overdue_books'] = BorrowReturnReceipt.objects.filter(
            return_date__isnull=True,
            due_date__lt=date.today()
        ).count()
    
    return render(request, 'app/home.html', context)


# ==================== AUTHENTICATION ====================

def login_view(request):
    """
    Đăng nhập hệ thống
    Dành cho: SuperUser, Staff (Quản lý, Thủ thư)
    """
    # Nếu đã đăng nhập, chuyển về trang chủ
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LibraryLoginForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Case-insensitive lookup
            user_obj = User.objects.filter(username__iexact=username).first()
            if not user_obj:
                 # User not found. Let form validation handle the error generation naturally.
                 pass
            else:
                # Check inactive status first
                if not user_obj.is_active:
                    messages.error(request, 'Tài khoản chưa được kích hoạt. Vui lòng liên hệ Admin.')
                else:
                    try:
                        # Logic for LibraryUser (tracking attempts)
                        lib_user = user_obj.library_user
                        
                        # Check lockout
                        if lib_user.failed_login_attempts >= 5:
                            form.add_error(None, 'Tài khoản đã bị khoá do đăng nhập sai quá 5 lần. Vui lòng liên hệ Admin hoặc sử dụng chức năng "Quên mật khẩu" để lấy lại mật khẩu.')
                        else:
                            # Attempt authentication with canonical username
                            user = authenticate(request, username=user_obj.username, password=password)
                            
                            if user:
                                # Success -> Reset counter
                                lib_user.failed_login_attempts = 0
                                lib_user.save(update_fields=['failed_login_attempts'])
                                login(request, user)
                                
                                # Welcome message
                                if user.is_superuser:
                                    messages.success(request, f'Chào mừng Quản trị viên {user.username}! Bạn có toàn quyền truy cập.')
                                elif user.is_staff:
                                    messages.success(request, f'Chào mừng {user.username}!')
                                else:
                                    messages.warning(request, 'Tài khoản này không có quyền truy cập hệ thống.')
                                    logout(request)
                                    return redirect('login')
                                
                                next_url = request.GET.get('next', 'home')
                                return redirect(next_url)
                            else:
                                # Failed password -> Increment counter
                                lib_user.failed_login_attempts += 1
                                lib_user.save(update_fields=['failed_login_attempts'])
                                
                                remaining = 5 - lib_user.failed_login_attempts
                                if remaining <= 0:
                                    form.add_error(None, 'Tài khoản đã bị khoá do đăng nhập sai quá 5 lần. Vui lòng liên hệ Admin hoặc sử dụng chức năng "Quên mật khẩu" để lấy lại mật khẩu.')
                                else:
                                    # Trigger validation to ensure errors dict is initialized
                                    _ = form.errors
                                    
                                    from django.utils.safestring import mark_safe
                                    from django.forms.utils import ErrorList
                                    
                                    # Custom message as requested: just "Wrong password..."
                                    combined_msg = mark_safe(f"Sai mật khẩu. Bạn còn {remaining} lần thử.")
                                    
                                    # Overwrite non-field errors to prevent duplication
                                    form.errors['__all__'] = ErrorList([combined_msg])
                    
                    except (AttributeError, User.library_user.RelatedObjectDoesNotExist):
                        # Fallback for users without LibraryUser (e.g. pure superuser)
                        if form.is_valid():
                            user = form.get_user()
                            login(request, user)
                            
                            # Welcome message
                            if user.is_superuser:
                                messages.success(request, f'Chào mừng Quản trị viên {user.username}! Bạn có toàn quyền truy cập.')
                            elif user.is_staff:
                                messages.success(request, f'Chào mừng {user.username}!')
                            else:
                                messages.warning(request, 'Tài khoản này không có quyền truy cập hệ thống.')
                                logout(request)
                                return redirect('login')
                            
                            next_url = request.GET.get('next', 'home')
                            return redirect(next_url)
                        else:
                            # Failed password -> Increment counter
                            lib_user.failed_login_attempts += 1
                            lib_user.save(update_fields=['failed_login_attempts'])
                            
                            remaining = 5 - lib_user.failed_login_attempts
                            if remaining <= 0:
                                form.add_error(None, 'Tài khoản đã bị khoá do đăng nhập sai quá 5 lần. Vui lòng liên hệ Admin hoặc sử dụng chức năng "Quên mật khẩu" để lấy lại mật khẩu.')
                            else:
                                # Trigger validation to ensure errors dict is initialized
                                _ = form.errors
                                
                                from django.utils.safestring import mark_safe
                                from django.forms.utils import ErrorList
                                
                                # Custom message as requested: just "Wrong password..."
                                combined_msg = mark_safe(f"Sai mật khẩu. Bạn còn {remaining} lần thử.")
                                
                                # Overwrite non-field errors to prevent duplication
                                form.errors['__all__'] = ErrorList([combined_msg])
                
                    except (AttributeError, ObjectDoesNotExist):
                        # Fallback for users without LibraryUser (e.g. pure superuser)
                        if form.is_valid():
                            user = form.get_user()
                            login(request, user)
                            if user.is_superuser:
                                messages.success(request, f'Chào mừng Quản trị viên {user.username}! Bạn có toàn quyền truy cập.')
                            
                            next_url = request.GET.get('next', 'home')
                            return redirect(next_url)
                        else:
                            # Form validation (triggered by is_valid) already added the error.
                            pass
        else:
             # User not found. Let form validation handle the error generation naturally.
             pass
    else:
        form = LibraryLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Đăng nhập'
    }
    
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """Đăng xuất khỏi hệ thống"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Đã đăng xuất tài khoản {username}.')
    return redirect('/')


from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.conf import settings
from urllib.parse import urlparse
from .forms import UserEmailPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = UserEmailPasswordResetForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Quên mật khẩu'
        return context

    def form_valid(self, form):
        # Determine which URL info to use
        # Logic: 
        # 1. Start with LOCAL_URL as default
        # 2. If PUBLIC_URL is defined AND (we are not in DEBUG OR request host matches public domain), use PUBLIC_URL
        
        target_url = settings.LOCAL_URL
        public_url = settings.PUBLIC_URL
        
        if public_url:
            # Parse public url to get domain
            try:
                public_parts = urlparse(public_url)
                request_host = self.request.get_host()
                
                # If the current request is coming from the public domain, OR we strictly want to valid public url usage
                # A simple heuristic: if request host is part of public url, use it.
                # However, user said: "If tunnel...". Tunnel often means request host IS the public domain.
                # But sometimes proxy setup is tricky. 
                # Let's trust the user's intent: If PUBLIC_URL is set, we prefer it if we are accessing via that domain
                # OR if DEBUG is False (Production/Tunnel mode assumption).
                
                if public_parts.netloc in request_host or not settings.DEBUG:
                    target_url = public_url
            except:
                pass
        
        # Extract domain and protocol from target_url
        parsed = urlparse(target_url)
        domain = parsed.netloc
        scheme = parsed.scheme
        use_https = (scheme == 'https')
        
        opts = {
            'use_https': use_https,
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
            'domain_override': domain,
        }
        form.save(**opts)
        return redirect(self.get_success_url())

# Rename to match urls.py expectation or update urls.py
password_reset_view = CustomPasswordResetView.as_view()


@login_required
def user_profile_view(request):
    """
    Trang cá nhân của người dùng
    Cho phép xem và cập nhật thông tin cá nhân
    """
    user = request.user
    
    if request.method == 'POST':
        # Cập nhật thông tin cơ bản
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validate email
        if email and User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Email đã được sử dụng bởi người dùng khác.')
        else:
            user.first_name = first_name
            user.last_name = last_name
            if email:
                user.email = email
            user.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
        
        # Đổi mật khẩu nếu có
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if old_password and new_password:
            if not user.check_password(old_password):
                messages.error(request, 'Mật khẩu cũ không đúng.')
            elif new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới và xác nhận không khớp.')
            elif len(new_password) < 6:
                messages.error(request, 'Mật khẩu mới phải có ít nhất 6 ký tự.')
            else:
                user.set_password(new_password)
                user.save()
                # Re-login để giữ session
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
                messages.success(request, 'Đổi mật khẩu thành công!')
        
        return redirect('user_profile')
    
    context = {
        'page_title': 'Trang cá nhân',
        'profile_user': user,
    }
    
    return render(request, 'accounts/profile.html', context)


# ==================== YC1: LẬP THẺ ĐỘC GIẢ ====================

@permission_required('Lập thẻ độc giả', 'add')
def reader_create_view(request):
    """
    View lập thẻ độc giả mới - YC1
    
    Business Rules (QĐ1):
    - Tuổi từ min_age đến max_age (mặc định 18-55)
    - Phải chọn loại độc giả hợp lệ
    - Thẻ có giá trị theo card_validity_period (mặc định 6 tháng)
    """
    
    # Kiểm tra hệ thống đã được cấu hình chưa
    params = Parameter.objects.first()
    if not params:
        messages.error(request, 'Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Lưu độc giả (auto-calculate expiration_date trong model.save())
                    reader = form.save()
                    
                    messages.success(
                        request,
                        f'Lập thẻ độc giả thành công! '
                        f'Mã độc giả: {reader.id} - {reader.reader_name}. '
                        f'Thẻ có hiệu lực đến: {reader.expiration_date.strftime("%d/%m/%Y")}'
                    )
                    return redirect('reader_detail', reader_id=reader.id)
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = ReaderForm()
    
    context = {
        'form': form,
        'params': params,
        'reader_types': ReaderType.objects.all(),
        'page_title': 'Lập thẻ độc giả mới'
    }
    
    return render(request, 'app/readers/reader_create.html', context)

@permission_required('Quản lý độc giả', 'view')
def reader_detail_view(request, reader_id):
    """
    Xem chi tiết thẻ độc giả - Hiển thị thông tin sau khi lập thẻ
    """
    reader = get_object_or_404(Reader, id=reader_id)
    
    context = {
        'reader': reader,
        'page_title': f'Thẻ độc giả - {reader.reader_name}'
    }
    
    return render(request, 'app/readers/reader_detail.html', context)


@permission_required('Quản lý độc giả', 'view')
def reader_list_view(request):
    """
    Danh sách độc giả - Để tra cứu và quản lý
    """
    readers = Reader.objects.select_related('reader_type').all().order_by('-card_creation_date')
    
    # Filter theo loại độc giả nếu có
    reader_type_id = request.GET.get('reader_type')
    if reader_type_id:
        readers = readers.filter(reader_type_id=reader_type_id)
    
    # Search theo tên hoặc email
    search_query = request.GET.get('search')
    if search_query:
        readers = readers.filter(
            reader_name__icontains=search_query
        ) | readers.filter(
            email__icontains=search_query
        )
    
    context = {
        'readers': readers,
        'reader_types': ReaderType.objects.all(),
        'page_title': 'Danh sách độc giả'
    }
    
    return render(request, 'app/readers/reader_list.html', context)


# ==================== YC2: TIẾP NHẬN SÁCH MỚI ====================

@permission_required('Lập phiếu nhập sách', 'add')
def book_import_view(request):
    """
    View tiếp nhận sách mới - YC2
    
    Business Rules (QĐ2):
    - Chỉ nhận sách xuất bản trong vòng 8 năm (book_return_period)
    - Thể loại phải hợp lệ
    - Tác giả phải hợp lệ
    - Tạo phiếu nhập và chi tiết phiếu nhập
    """
    
    # Kiểm tra hệ thống đã được cấu hình chưa
    params = Parameter.objects.first()
    if not params:
        messages.error(request, 'Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.')
        return redirect('home')
    
    if request.method == 'POST':
        form = BookImportForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Lấy dữ liệu từ form
                    book_title_name = form.cleaned_data['book_title']
                    category = form.cleaned_data['category']
                    authors = list(form.cleaned_data['authors']) # Convert to list to append new ones
                    new_authors_str = form.cleaned_data.get('new_authors', '')
                    
                    publish_year = form.cleaned_data['publish_year']
                    publisher = form.cleaned_data['publisher']
                    isbn = form.cleaned_data.get('isbn', '')
                    edition = form.cleaned_data.get('edition', '')
                    language = form.cleaned_data['language']
                    quantity = form.cleaned_data['quantity']
                    unit_price = form.cleaned_data['unit_price']
                    description = form.cleaned_data.get('description', '')
                    notes = form.cleaned_data.get('notes', '')
                    import_date = form.cleaned_data['import_date']
                    
                    # Xử lý tác giả mới
                    if new_authors_str:
                        new_author_names = [name.strip() for name in new_authors_str.split(',') if name.strip()]
                        for name in new_author_names:
                            # Tìm hoặc tạo tác giả mới (không phân biệt hoa thường để tránh trùng lặp)
                            # Tuy nhiên, models.Author không có constraint unique=True cho author_name
                            # Nên ta dùng get_or_create đơn giản
                            author, _ = Author.objects.get_or_create(author_name=name)
                            if author not in authors:
                                authors.append(author)
                    
                    # Kiểm tra hoặc tạo BookTitle
                    book_title, created = BookTitle.objects.get_or_create(
                        book_title=book_title_name,
                        category=category,
                        defaults={'description': description}
                    )
                    
                    # Thêm tác giả cho BookTitle (cả cũ và mới)
                    # Nếu BookTitle đã tồn tại, ta vẫn nên kiểm tra xem có cần bổ sung tác giả không?
                    # Logic hiện tại: chỉ thêm nếu created=True. 
                    # Nếu BookTitle đã có, ta có thể muốn update thêm tác giả nếu chưa có?
                    # Để an toàn và nhất quán với yêu cầu, ta sẽ add thêm tác giả vào BookTitle nếu chưa có logic đó.
                    # Nhưng code cũ chỉ thêm khi created. Ta sẽ giữ nguyên logic đó hoặc cải tiến.
                    # Quyết định: Cập nhật connection tác giả cho BookTitle dù mới hay cũ
                    
                    current_authors = book_title.authors.all()
                    for author in authors:
                        if author not in current_authors:
                            AuthorDetail.objects.create(
                                author=author,
                                book_title=book_title
                            )
                    
                    # Tạo hoặc cập nhật Book
                    book, book_created = Book.objects.get_or_create(
                        book_title=book_title,
                        publish_year=publish_year,
                        publisher=publisher,
                        isbn=isbn if isbn else None,
                        defaults={
                            'quantity': quantity,  # Dùng quantity từ form, không hardcode!
                            'remaining_quantity': quantity,  # Ban đầu = quantity (chưa mượn)
                            'unit_price': unit_price,
                            'edition': edition,
                            'language': language
                        }
                    )
                    
                    # Nếu book đã tồn tại, cập nhật số lượng
                    if not book_created:
                        book.quantity += quantity
                        book.remaining_quantity += quantity
                        book.save(update_fields=['quantity', 'remaining_quantity'])
                    
                    # Tạo phiếu nhập
                    receipt = BookImportReceipt.objects.create(
                        import_date=import_date,
                        created_by=request.user.username,
                        notes=notes
                    )
                    
                    # Tạo chi tiết phiếu nhập
                    import_detail = BookImportDetail.objects.create(
                        receipt=receipt,
                        book=book,
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    
                    # Thông báo thành công
                    messages.success(
                        request,
                        f'Tiếp nhận sách thành công! '
                        f'Tựa sách: {book_title.book_title} '
                        f'({quantity} cuốn, {unit_price:,}đ/cuốn). '
                        f'Phiếu nhập #{receipt.id}.'
                    )
                    return redirect('book_import_detail', import_id=receipt.id)
            except ValidationError as e:
                # Lỗi validation từ model
                messages.error(request, f'Lỗi validation: {e.message if hasattr(e, "message") else str(e)}')
            except Exception as e:
                # Lỗi hệ thống khác
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        else:
            # Hiển thị lỗi validation cho user
            for field, errors in form.errors.items():
                # Lấy label thân thiện từ form field
                field_label = form.fields[field].label if field in form.fields else field
                for error in errors:
                    messages.error(request, f'{field_label}: {error}')
    else:
        form = BookImportForm()
    
    # Lấy tham số để hiển thị thông tin QĐ2
    from datetime import date
    min_year = date.today().year - params.book_return_period
    
    context = {
        'form': form,
        'params': params,
        'min_year': min_year,
        'page_title': 'Tiếp nhận sách mới'
    }
    
    return render(request, 'app/books/book_import.html', context)


@permission_required('Lập phiếu nhập sách', 'view')
def book_import_detail_view(request, import_id):
    """
    Xem chi tiết phiếu nhập sách
    """
    receipt = get_object_or_404(BookImportReceipt, id=import_id)
    import_details = receipt.import_details.all()
    
    context = {
        'receipt': receipt,
        'import_details': import_details,
        'page_title': f'Phiếu nhập sách #{receipt.id}'
    }
    
    return render(request, 'app/books/book_import_detail.html', context)


@permission_required('Lập phiếu nhập sách', 'view')
def book_import_list_view(request):
    """
    Danh sách phiếu nhập sách
    """
    receipts = BookImportReceipt.objects.all().order_by('-import_date')
    
    # Filter theo tháng/năm nếu có
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    # Validate Inputs
    try:
        if year:
            year_int = int(year)
            import datetime
            current_year = datetime.datetime.now().year
            if not (2000 <= year_int <= current_year):
                messages.warning(request, f'Năm "{year}" không hợp lệ. Vui lòng nhập năm từ 2000 đến {current_year}.')
                year = None
    except ValueError:
        messages.warning(request, f'Năm "{year}" không hợp lệ. Vui lòng nhập số.')
        year = None

    try:
        if month:
            month_int = int(month)
            if not (1 <= month_int <= 12):
                month = None
    except ValueError:
        month = None
    
    if month and year:
        receipts = receipts.filter(
            import_date__month=month,
            import_date__year=year
        )
    elif year:
        receipts = receipts.filter(import_date__year=year)
    
    context = {
        'receipts': receipts,
        'page_title': 'Danh sách phiếu nhập sách'
    }
    
    return render(request, 'app/books/book_import_list.html', context)


# ==================== BOOK SEARCH (YC3) ====================

def book_search_view(request):
    """
    Tra cứu sách - YC3
    Chức năng công khai - ai cũng có thể tra cứu
    """
    from django.db.models import Q
    
    form = BookSearchForm(request.GET)
    books = Book.objects.all().select_related('book_title', 'book_title__category').prefetch_related('book_title__authors')
    
    if form.is_valid():
        # Tìm kiếm theo tên sách hoặc mã sách
        search_text = form.cleaned_data.get('search_text')
        if search_text:
            books = books.filter(
                Q(book_title__book_title__icontains=search_text) |
                Q(id__icontains=search_text)
            )
        
        # Lọc theo thể loại
        category = form.cleaned_data.get('category')
        if category:
            books = books.filter(book_title__category=category)
        
        # Lọc theo tác giả
        author = form.cleaned_data.get('author')
        if author:
            books = books.filter(book_title__authors=author)
        
        # Lọc theo tình trạng
        status = form.cleaned_data.get('status')
        if status == 'available':
            books = books.filter(remaining_quantity__gt=0)
        elif status == 'unavailable':
            books = books.filter(remaining_quantity=0)
    
    # Sắp xếp theo tên sách
    books = books.order_by('book_title__book_title')
    
    # Phân trang (20 cuốn/trang)
    from django.core.paginator import Paginator
    paginator = Paginator(books, 20)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'books': page_obj.object_list,
        'total_results': paginator.count,
        'page_title': 'Tra cứu sách'
    }
    
    return render(request, 'app/books/book_search.html', context)


# ==================== BORROW BOOK (YC4) ====================

@permission_required('Lập phiếu mượn sách', 'add')
def borrow_book_view(request):
    """
    Cho mượn sách - YC4
    Validate theo thẻ còn hạn, không quá hạn, sách chưa mượn, không quá 5 quyển
    Hỗ trợ mượn nhiều sách cùng lúc
    """
    params = Parameter.objects.first()
    
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    reader_id = form.cleaned_data['reader_id']
                    book_ids = form.cleaned_data['book_ids']  # List of IDs
                    borrow_date = form.cleaned_data['borrow_date']
                    books = form.cleaned_data['books']  # Dict of Book objects
                    
                    # Lấy độc giả
                    reader = Reader.objects.get(id=reader_id)
                    
                    # Tính ngày phải trả (tối đa 4 ngày)
                    from datetime import datetime, timedelta
                    borrow_datetime = datetime.combine(borrow_date, datetime.min.time())
                    borrow_datetime = timezone.make_aware(borrow_datetime)
                    due_date = borrow_datetime + timedelta(days=params.max_borrow_days)
                    
                    # Tạo phiếu mượn cho từng sách
                    receipts = []
                    for book_id in book_ids:
                        book = books[book_id]
                        
                        # Lấy cuốn sách còn sẵn (lock row to prevent race condition)
                        book_item = BookItem.objects.select_for_update().filter(book=book, is_borrowed=False).first()
                        if not book_item:
                            messages.error(request, f'Không tìm thấy cuốn "{book.book_title.book_title}" còn sẵn.')
                            return redirect('borrow_book')
                        
                        # Tạo phiếu mượn
                        borrow_receipt = BorrowReturnReceipt.objects.create(
                            reader=reader,
                            book_item=book_item,
                            borrow_date=borrow_datetime,
                            due_date=due_date,
                            notes=''
                        )
                        receipts.append(borrow_receipt)
                        
                        # Cập nhật trạng thái cuốn sách
                        book_item.is_borrowed = True
                        book_item.save(update_fields=['is_borrowed'])
                        
                        # Cập nhật số lượng còn lại của sách
                        book.remaining_quantity -= 1
                        book.save(update_fields=['remaining_quantity'])
                    
                    # Thông báo thành công
                    if len(receipts) == 1:
                        messages.success(
                            request,
                            f'Cho mượn thành công! Phiếu #{receipts[0].id} - Phải trả trước {due_date.strftime("%d/%m/%Y")}'
                        )
                        return redirect('borrow_book_detail', receipt_id=receipts[0].id)
                    else:
                        receipt_ids = ', '.join([f'#{r.id}' for r in receipts])
                        messages.success(
                            request,
                            f'Cho mượn {len(receipts)} quyển thành công! Phiếu: {receipt_ids} - Phải trả trước {due_date.strftime("%d/%m/%Y")}'
                        )
                        return redirect('borrow_book_list')
                    
            except Reader.DoesNotExist:
                messages.error(request, 'Độc giả không tồn tại.')
                return redirect('borrow_book')
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
                return redirect('borrow_book')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = BorrowBookForm()
    
    context = {
        'form': form,
        'params': params,
        'page_title': 'Cho mượn sách'
    }
    
    return render(request, 'app/borrowing/borrow_book.html', context)


@permission_required('Quản lý mượn/trả', 'view')
def borrow_book_detail_view(request, receipt_id):
    """
    Xem chi tiết phiếu mượn sách
    """
    receipt = get_object_or_404(BorrowReturnReceipt, id=receipt_id)
    
    context = {
        'receipt': receipt,
        'page_title': f'Phiếu mượn #{receipt.id}'
    }
    
    return render(request, 'app/borrowing/borrow_book_detail.html', context)


@permission_required('Quản lý mượn/trả', 'view')
def borrow_book_list_view(request):
    """
    Danh sách phiếu mượn sách
    """
    from django.db.models import Q
    from django.utils import timezone
    
    # Mặc định sort
    receipts = BorrowReturnReceipt.objects.filter(return_date__isnull=True).order_by('-borrow_date')
    
    # Filter theo trạng thái
    status = request.GET.get('status', 'unreturned')
    if status == 'all':
        receipts = BorrowReturnReceipt.objects.all().order_by('-borrow_date')
    elif status == 'overdue':
        receipts = receipts.filter(due_date__lt=timezone.now())
    
    # Search
    search = request.GET.get('search', '')
    if search:
        receipts = receipts.filter(
            Q(reader__reader_name__icontains=search) |
            Q(book_item__book__book_title__book_title__icontains=search) |
            Q(reader__email__icontains=search) |
            Q(id__icontains=search)
        )
    
    # Filter theo độc giả (giữ lại logic cũ phòng khi dùng)
    reader_id = request.GET.get('reader_id')
    if reader_id:
        receipts = receipts.filter(reader_id=reader_id)
        
    # Phân trang
    from django.core.paginator import Paginator
    paginator = Paginator(receipts, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'receipts': page_obj.object_list,
        'current_status': status,
        'search': search,
        'total_results': paginator.count,
        'page_title': 'Danh sách phiếu mượn sách'
    }
    
    return render(request, 'app/borrowing/borrow_book_list.html', context)


# ==================== API ENDPOINTS FOR BORROW BOOK ====================

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

@permission_required('Quản lý độc giả', 'view')
@require_http_methods(["GET"])
def api_readers_list(request):
    """
    API lấy danh sách độc giả với tìm kiếm
    Query params: search (tìm kiếm theo tên hoặc email)
    """
    search = request.GET.get('search', '').strip()
    
    # Chỉ hiện độc giả hoạt động
    readers = Reader.objects.filter(is_active=True).order_by('reader_name')
    
    if search:
        readers = readers.filter(
            Q(reader_name__icontains=search) | 
            Q(email__icontains=search)
        )
    
    data = [
        {
            'id': reader.id,
            'name': reader.reader_name,
            'email': reader.email,
            'display': f"{reader.reader_name} - {reader.email}"
        }
        for reader in readers[:50]  # Giới hạn 50 kết quả
    ]
    
    return JsonResponse({'success': True, 'data': data})


@permission_required('Quản lý kho sách', 'view')
@require_http_methods(["GET"])
def api_books_list(request):
    """
    API lấy danh sách sách còn sẵn với tìm kiếm
    Query params: search (tìm kiếm theo tên sách hoặc tác giả)
    """
    search = request.GET.get('search', '').strip()
    
    # Chỉ hiện sách còn sẵn
    books = Book.objects.filter(remaining_quantity__gt=0).select_related(
        'book_title', 'book_title__category'
    ).order_by('book_title__book_title')
    
    if search:
        books = books.filter(
            Q(book_title__book_title__icontains=search) |
            Q(book_title__authors__author_name__icontains=search)
        ).distinct()
    
    data = [
        {
            'id': book.id,
            'title': book.book_title.book_title,
            'year': book.publish_year,
            'category': book.book_title.category.category_name if book.book_title.category else 'N/A',
            'remaining': book.remaining_quantity,
            'display': f"{book.book_title.book_title} ({book.publish_year}) - Còn {book.remaining_quantity} quyển"
        }
        for book in books[:50]  # Giới hạn 50 kết quả
    ]
    
    return JsonResponse({'success': True, 'data': data})


@permission_required('Quản lý mượn/trả', 'view')
@require_http_methods(["GET"])
def api_borrowing_readers(request):
    """
    API lấy danh sách độc giả đang mượn sách (chưa trả)
    """
    # Lấy tất cả phiếu mượn chưa trả, group by reader
    from django.db.models import Count, Max
    
    borrowing_records = BorrowReturnReceipt.objects.filter(
        return_date__isnull=True
    ).values('reader_id').annotate(
        count=Count('id'),
        latest_due=Max('due_date')
    ).order_by('-latest_due')
    
    records = list(borrowing_records[:100])  # Giới hạn 100 kết quả
    reader_ids = [r['reader_id'] for r in records]
    readers_map = Reader.objects.filter(id__in=reader_ids).in_bulk()
    
    data = []
    for record in records:
        if record['reader_id'] not in readers_map:
            continue
            
        reader = readers_map[record['reader_id']]
        
        # Lấy danh sách sách đang mượn
        borrows = BorrowReturnReceipt.objects.filter(
            reader_id=reader.id,
            return_date__isnull=True
        ).select_related('book_item__book__book_title')
        
        # Kiểm tra có quá hạn không
        from django.utils import timezone
        today = timezone.now().date()
        is_overdue = any(b.due_date.date() < today for b in borrows)
        
        data.append({
            'reader_id': reader.id,
            'reader_name': reader.reader_name,
            'reader_email': reader.email,
            'borrowed_count': record['count'],
            'latest_due_date': record['latest_due'].strftime('%d/%m/%Y'),
            'is_overdue': is_overdue,
            'books': [
                {
                    'title': b.book_item.book.book_title.book_title,
                    'borrow_date': b.borrow_date.strftime('%d/%m/%Y'),
                    'due_date': b.due_date.strftime('%d/%m/%Y'),
                    'is_overdue': b.due_date.date() < today
                }
                for b in borrows
            ]
        })
    
    return JsonResponse({'success': True, 'data': data})
"""
Views cho YC5: Nhận trả sách
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import BorrowReturnReceipt, Parameter, Reader
from .forms import ReturnBookForm


@permission_required('Lập phiếu trả sách', 'add')
def return_book_view(request):
    """
    Trang nhận trả sách - YC5
    Chọn độc giả → chọn sách → nhập ngày trả
    """
    params = Parameter.objects.first()
    fine_rate = params.fine_rate if params else 1000
    
    context = {
        'page_title': 'Nhận trả sách',
        'params': params,
        'fine_rate': fine_rate,
    }
    
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            receipts = form.save()
            if receipts:
                count = len(receipts)
                # Lấy reader từ receipt đầu tiên và kiểm tra nợ
                reader = receipts[0].reader if receipts else None
                if reader and reader.total_debt > 0:
                    messages.success(
                        request, 
                        f'Đã ghi nhận trả sách - {count} quyển. '
                        f'Độc giả còn nợ {reader.total_debt:,}đ. '
                        f'<a href="/receipt/" class="text-blue-600 underline font-semibold">Lập phiếu thu ngay</a>',
                        extra_tags='safe'
                    )
                else:
                    messages.success(request, f'Đã ghi nhận trả sách - {count} quyển')
                return redirect('return_book_list')
            else:
                messages.error(request, 'Lỗi khi lưu thông tin trả sách')
    else:
        form = ReturnBookForm()
    
    # Convert params to JSON for JavaScript
    import json
    params_json = json.dumps({
        'fine_rate': params.fine_rate if params else 1000
    })
    
    # Get all readers for dropdown
    readers = Reader.objects.all().values('id', 'reader_name', 'email').order_by('reader_name')
    
    context['form'] = form
    context['params_json'] = params_json
    context['readers'] = list(readers)
    context['readers_json'] = json.dumps(list(readers))
    return render(request, 'app/borrowing/return_book.html', context)


@permission_required('Lập phiếu trả sách', 'view')
def return_book_detail_view(request, receipt_id):
    """
    Xem chi tiết phiếu trả sách - YC5
    Hiển thị: thông tin độc giả, sách trả, tiền phạt
    """
    receipt = get_object_or_404(BorrowReturnReceipt, id=receipt_id)
    params = Parameter.objects.first()
    fine_rate = params.fine_rate if params else 1000
    
    # Tính tiền phạt
    days_overdue = receipt.days_overdue if receipt.is_overdue else 0
    fine_amount = days_overdue * fine_rate
    
    context = {
        'page_title': f'Chi tiết phiếu trả sách #{receipt_id}',
        'receipt': receipt,
        'days_overdue': days_overdue,
        'fine_amount': fine_amount,
        'fine_rate': fine_rate,
    }
    
    return render(request, 'app/borrowing/return_book_detail.html', context)


@permission_required('Lập phiếu trả sách', 'view')
def return_book_list_view(request):
    """
    Danh sách phiếu trả sách - YC5
    Hỗ trợ lọc và tìm kiếm
    """
    # Lấy bộ lọc từ GET
    filter_type = request.GET.get('filter', 'all')
    search = request.GET.get('search', '')
    
    # Base query: chỉ lấy phiếu đã trả (return_date != null)
    receipts = BorrowReturnReceipt.objects.filter(
        return_date__isnull=False
    ).select_related('reader', 'book_item__book__book_title')
    
    # Lọc theo loại
    if filter_type == 'overdue':
        from django.db.models import Q
        receipts = receipts.filter(
            due_date__date__lt=models.F('return_date__date')
        )
    elif filter_type == 'ontime':
        from django.db.models import Q, F as DjangoF
        receipts = receipts.exclude(
            due_date__date__lt=DjangoF('return_date__date')
        )
    
    # Tìm kiếm theo tên độc giả hoặc tên sách
    if search:
        from django.db.models import Q
        receipts = receipts.filter(
            Q(reader__reader_name__icontains=search) |
            Q(book_item__book__book_title__book_title__icontains=search) |
            Q(reader__email__icontains=search)
        )
    
    # Sắp xếp
    receipts = receipts.order_by('-return_date')
    
    # Phân trang
    from django.core.paginator import Paginator
    paginator = Paginator(receipts, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Tính tiền phạt cho mỗi receipt
    for receipt in page_obj.object_list:
        if hasattr(receipt, 'is_overdue') and receipt.is_overdue:
            receipt.fine_amount = receipt.days_overdue * 1000  # 1000đ/ngày
        else:
            receipt.fine_amount = 0
    
    context = {
        'page_title': 'Danh sách phiếu trả sách',
        'page_obj': page_obj,
        'receipts': page_obj.object_list,
        'filter_type': filter_type,
        'search': search,
        'total_results': paginator.count,
    }
    
    return render(request, 'app/borrowing/return_book_list.html', context)


@login_required
@permission_required('Lập phiếu trả sách', 'view')
@require_http_methods(["GET"])
def api_unreturned_receipts(request):
    """
    API: Lấy danh sách phiếu mượn chưa trả
    Dùng cho dropdown chọn phiếu trả sách
    """
    search = request.GET.get('search', '')
    print(f'[API] Fetching unreturned receipts, search={search}')
    
    # Lấy phiếu chưa trả
    receipts = BorrowReturnReceipt.objects.filter(
        return_date__isnull=True
    ).select_related('reader', 'book_item__book__book_title')
    
    print(f'[API] Found {len(receipts)} unreturned receipts')
    
    # Tìm kiếm
    if search:
        from django.db.models import Q
        receipts = receipts.filter(
            Q(reader__reader_name__icontains=search) |
            Q(book_item__book__book_title__book_title__icontains=search) |
            Q(reader__email__icontains=search) |
            Q(id__icontains=search)
        )
    
    # Giới hạn kết quả
    receipts = receipts[:50]
    
    data = []
    for receipt in receipts:
        try:
            days_borrowed = (timezone.now().date() - receipt.borrow_date.date()).days
            book_title = receipt.book_item.book.book_title.book_title
            reader_name = receipt.reader.reader_name
            
            data.append({
                'id': receipt.id,
                'reader_name': reader_name,
                'reader_email': receipt.reader.email,
                'book_title': book_title,
                'borrow_date': receipt.borrow_date.strftime('%d/%m/%Y'),
                'due_date': receipt.due_date.strftime('%d/%m/%Y'),
                'days_borrowed': days_borrowed,
                'is_overdue': receipt.due_date.date() < timezone.now().date(),
                'display': f"#{receipt.id} - {reader_name} ({book_title})"
            })
        except Exception as e:
            print(f'Error processing receipt {receipt.id}: {e}')
            continue
    
    return JsonResponse({'success': True, 'data': data})


@login_required
@permission_required('Quản lý mượn/trả', 'view')
@require_http_methods(["GET"])
def api_reader_borrowed_books(request, reader_id):
    """
    API: Lấy danh sách sách độc giả đó mượn nhưng chưa trả
    """
    try:
        reader = Reader.objects.get(id=reader_id)
    except Reader.DoesNotExist:
        return JsonResponse({'success': False, 'data': [], 'error': 'Reader not found'}, status=404)
    
    # Lấy danh sách phiếu mượn chưa trả của độc giả
    receipts = BorrowReturnReceipt.objects.filter(
        reader=reader,
        return_date__isnull=True
    ).select_related('book_item__book__book_title')
    
    data = []
    for receipt in receipts:
        try:
            days_borrowed = (timezone.now().date() - receipt.borrow_date.date()).days
            book_title = receipt.book_item.book.book_title.book_title
            days_overdue = max(0, days_borrowed - 4)
            
            data.append({
                'receipt_id': receipt.id,
                'book_item_id': receipt.book_item.id,
                'book_title': book_title,
                'barcode': receipt.book_item.barcode,
                'borrow_date': receipt.borrow_date.strftime('%d/%m/%Y'),
                'due_date': receipt.due_date.strftime('%d/%m/%Y'),
                'days_borrowed': days_borrowed,
                'days_overdue': days_overdue,
                'is_overdue': days_overdue > 0,
            })
        except Exception as e:
            print(f'Error processing receipt {receipt.id}: {e}')
            continue
    
    return JsonResponse({'success': True, 'data': data})


# ==================== PAYMENT MANAGEMENT (YC6) ====================

@permission_required('Lập phiếu thu tiền phạt', 'add')
def receipt_form_view(request):
    """
    Lập phiếu thu tiền phạt - YC6 (BM6)
    GET: Hiển thị form chọn độc giả → hiển thị nợ → nhập số tiền → submit
    POST: Xử lý submit, kiểm tra QĐ6, lưu phiếu, trừ nợ
    """
    import json
    
    # Lấy danh sách độc giả có nợ
    readers_with_debt = Reader.objects.filter(
        total_debt__gt=0
    ).values('id', 'reader_name', 'email', 'total_debt')
    
    readers_json = json.dumps(list(readers_with_debt))
    
    # Lấy tham số hệ thống
    try:
        params = Parameter.objects.first()
    except:
        params = None
    
    if request.method == 'POST':
        # Kiểm tra quyền 'add' cho lập phiếu thu
        from .decorators import check_permission
        if not check_permission(request.user, 'Lập phiếu thu tiền phạt', 'add'):
            messages.error(request, 'Bạn không có quyền thêm phiếu thu tiền.')
            return redirect('receipt_list')
        
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()
            if receipt:
                messages.success(
                    request,
                    f'Đã ghi nhận thu tiền {receipt.collected_amount:,}đ từ {receipt.reader.reader_name}. '
                    f'Nợ còn lại: {receipt.reader.total_debt:,}đ'
                )
                return redirect('receipt_list')
            else:
                messages.error(request, 'Lỗi khi lưu phiếu thu tiền')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ReceiptForm()
    
    # Bank configuration for VietQR - Query from database
    bank_account = BankAccount.objects.filter(is_active=True).first()
    
    if bank_account:
        bank_config = {
            'bankId': bank_account.bank_id,
            'accountNo': bank_account.account_no,
            'accountName': bank_account.account_name,
            'template': bank_account.template
        }
    else:
        # Fallback nếu chưa có tài khoản trong DB
        bank_config = {
            'bankId': '',
            'accountNo': '',
            'accountName': '',
            'template': 'print'
        }
    
    context = {
        'form': form,
        'readers_json': readers_json,
        'params': params,
        'bank_config': json.dumps(bank_config),
    }
    
    return render(request, 'app/receipts/receipt_form.html', context)


@permission_required('Quản lý phiếu thu', 'view')
def receipt_list_view(request):
    """
    Danh sách phiếu thu tiền
    Hỗ trợ tìm kiếm, lọc theo ngày
    """
    search = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'reader_name')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    # Base query
    receipts = Receipt.objects.select_related('reader').order_by('-created_date')
    
    # Tìm kiếm
    if search and search_type == 'reader_name':
        from django.db.models import Q
        receipts = receipts.filter(
            Q(reader__reader_name__icontains=search) |
            Q(reader__email__icontains=search)
        )
    
    # Lọc theo ngày
    if from_date:
        receipts = receipts.filter(created_date__gte=from_date)
    if to_date:
        receipts = receipts.filter(created_date__lte=to_date)
    
    # Phân trang
    from django.core.paginator import Paginator
    paginator = Paginator(receipts, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Danh sách phiếu thu tiền',
        'page_obj': page_obj,
        'receipts': page_obj.object_list,
        'search': search,
        'search_type': search_type,
        'from_date': from_date,
        'to_date': to_date,
        'total_results': paginator.count,
    }
    
    return render(request, 'app/receipts/receipt_list.html', context)


@permission_required('Quản lý phiếu thu', 'view')
def receipt_detail_view(request, receipt_id):
    """
    Chi tiết phiếu thu tiền
    """
    receipt = get_object_or_404(Receipt, id=receipt_id)
    
    context = {
        'receipt': receipt,
        'page_title': f'Chi tiết phiếu thu #{receipt.id}'
    }
    
    return render(request, 'app/receipts/receipt_detail.html', context)


@login_required
@permission_required('Quản lý độc giả', 'view')
@require_http_methods(["GET"])
def api_reader_debt(request, reader_id):
    """
    API: Lấy thông tin nợ tiền phạt của độc giả
    """
    try:
        reader = Reader.objects.get(id=reader_id)
        
        return JsonResponse({
            'success': True,
            'reader_id': reader.id,
            'reader_name': reader.reader_name,
            'email': reader.email,
            'total_debt': reader.total_debt,
        })
    except Reader.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Độc giả không tồn tại'
        }, status=404)


# ==================== REPORTS - YC7 ====================

@permission_required('Báo cáo mượn sách theo thể loại', 'view')
def report_borrow_by_category_view(request):
    """
    YC7 - BM7.1: Báo cáo thống kê tình hình mượn sách theo thể loại
    """
    # Lấy tháng/năm từ request, mặc định là tháng hiện tại
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not month or not year:
        now = timezone.now()
        month = now.month
        year = now.year
    else:
        month = int(month)
        year = int(year)
    
    # Tính ngày đầu và cuối tháng
    from calendar import monthrange
    first_day = timezone.datetime(year, month, 1, tzinfo=timezone.get_current_timezone())
    last_day_num = monthrange(year, month)[1]
    last_day = timezone.datetime(year, month, last_day_num, 23, 59, 59, tzinfo=timezone.get_current_timezone())
    
    # Lấy danh sách phiếu mượn trong tháng (D3)
    borrow_receipts = BorrowReturnReceipt.objects.filter(
        borrow_date__gte=first_day,
        borrow_date__lte=last_day
    ).select_related('book_item__book__book_title__category')
    
    # Đếm số lượt mượn theo thể loại (D4)
    category_stats = {}
    total_borrows = 0
    
    for receipt in borrow_receipts:
        # Lấy thể loại từ book_item -> book -> book_title -> category
        if receipt.book_item and receipt.book_item.book:
            category = receipt.book_item.book.book_title.category
            category_name = category.category_name
            
            if category_name not in category_stats:
                category_stats[category_name] = 0
            
            category_stats[category_name] += 1
            total_borrows += 1
    
    # Tính tỉ lệ (%)
    report_data = []
    for idx, (category_name, borrow_count) in enumerate(sorted(category_stats.items()), start=1):
        percentage = (borrow_count / total_borrows * 100) if total_borrows > 0 else 0
        report_data.append({
            'stt': idx,
            'category_name': category_name,
            'borrow_count': borrow_count,
            'percentage': round(percentage, 2)
        })
    
    context = {
        'report_data': report_data,
        'total_borrows': total_borrows,
        'month': month,
        'year': year,
        'page_title': f'Báo cáo mượn sách theo thể loại - Tháng {month}/{year}'
    }
    
    return render(request, 'app/reports/report_borrow_by_category.html', context)


@permission_required('Báo cáo sách trả trễ', 'view')
def report_overdue_books_view(request):
    """
    YC7 - BM7.2: Báo cáo thống kê sách trả trễ
    """
    # Lấy ngày báo cáo từ request, mặc định là ngày hiện tại
    report_date_str = request.GET.get('report_date')
    
    if report_date_str:
        try:
            report_date = timezone.datetime.strptime(report_date_str, '%Y-%m-%d')
            report_date = timezone.make_aware(report_date, timezone.get_current_timezone())
        except ValueError:
            report_date = timezone.now()
    else:
        report_date = timezone.now()
    
    # Lấy danh sách phiếu mượn chưa trả và quá hạn (D3)
    # return_date = NULL và due_date < report_date
    overdue_receipts = BorrowReturnReceipt.objects.filter(
        return_date__isnull=True,  # Chưa trả
        due_date__lt=report_date   # Quá hạn
    ).select_related('book_item__book__book_title')
    
    # Tạo danh sách thống kê (D4)
    report_data = []
    for idx, receipt in enumerate(overdue_receipts, start=1):
        # Tính số ngày trễ
        overdue_days = (report_date.date() - receipt.due_date.date()).days
        
        book_title = receipt.book_item.book.book_title.book_title if receipt.book_item else "N/A"
        
        report_data.append({
            'stt': idx,
            'book_title': book_title,
            'borrow_date': receipt.borrow_date,
            'overdue_days': overdue_days
        })
    
    context = {
        'report_data': report_data,
        'report_date': report_date,
        'page_title': f'Báo cáo sách trả trễ - Ngày {report_date.strftime("%d/%m/%Y")}'
    }
    
    return render(request, 'app/reports/report_overdue_books.html', context)


@permission_required('Báo cáo mượn sách theo thể loại', 'view')
def report_borrow_by_category_excel(request):
    """
    Export báo cáo mượn sách theo thể loại ra file Excel
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    from django.http import HttpResponse
    from calendar import monthrange
    
    # Lấy tháng/năm từ request
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))
    
    # Tính ngày đầu và cuối tháng
    first_day = timezone.datetime(year, month, 1, tzinfo=timezone.get_current_timezone())
    last_day_num = monthrange(year, month)[1]
    last_day = timezone.datetime(year, month, last_day_num, 23, 59, 59, tzinfo=timezone.get_current_timezone())
    
    # Lấy dữ liệu
    borrow_receipts = BorrowReturnReceipt.objects.filter(
        borrow_date__gte=first_day,
        borrow_date__lte=last_day
    )
    
    category_stats = {}
    total_borrows = 0
    
    for receipt in borrow_receipts:
        if receipt.book_item and receipt.book_item.book:
            category_name = receipt.book_item.book.book_title.category.category_name
            category_stats[category_name] = category_stats.get(category_name, 0) + 1
            total_borrows += 1
    
    # Tạo workbook
    wb = Workbook()
    ws = wb.active
    ws.title = f"Mượn sách T{month}-{year}"
    
    # Style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = f'Báo cáo mượn sách theo thể loại - Tháng {month}/{year}'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Headers
    headers = ['STT', 'Tên thể loại', 'Số lượt mượn', 'Tỉ lệ (%)']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
    
    # Data
    row = 4
    for idx, (category_name, borrow_count) in enumerate(sorted(category_stats.items()), 1):
        percentage = round((borrow_count / total_borrows * 100), 2) if total_borrows > 0 else 0
        ws.cell(row=row, column=1, value=idx).border = thin_border
        ws.cell(row=row, column=2, value=category_name).border = thin_border
        ws.cell(row=row, column=3, value=borrow_count).border = thin_border
        ws.cell(row=row, column=4, value=f"{percentage}%").border = thin_border
        row += 1
    
    # Total
    ws.merge_cells(f'A{row}:B{row}')
    ws.cell(row=row, column=1, value='Tổng số lượt mượn:').font = Font(bold=True)
    ws.cell(row=row, column=3, value=total_borrows).font = Font(bold=True)
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12
    
    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_muon_sach_{month}_{year}.xlsx"'
    wb.save(response)
    return response


@permission_required('Báo cáo sách trả trễ', 'view')
def report_overdue_books_excel(request):
    """
    Export báo cáo sách trả trễ ra file Excel
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    from django.http import HttpResponse
    
    # Lấy ngày báo cáo
    report_date_str = request.GET.get('report_date')
    if report_date_str:
        try:
            report_date = timezone.datetime.strptime(report_date_str, '%Y-%m-%d')
            report_date = timezone.make_aware(report_date, timezone.get_current_timezone())
        except ValueError:
            report_date = timezone.now()
    else:
        report_date = timezone.now()
    
    # Lấy dữ liệu
    overdue_receipts = BorrowReturnReceipt.objects.filter(
        return_date__isnull=True,
        due_date__lt=report_date
    ).select_related('book_item__book__book_title')
    
    # Tạo workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sách trả trễ"
    
    # Style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = f'Báo cáo sách trả trễ - Ngày {report_date.strftime("%d/%m/%Y")}'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Headers
    headers = ['STT', 'Tên sách', 'Ngày mượn', 'Số ngày trễ']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
    
    # Data
    row = 4
    for idx, receipt in enumerate(overdue_receipts, 1):
        overdue_days = (report_date.date() - receipt.due_date.date()).days
        book_title = receipt.book_item.book.book_title.book_title if receipt.book_item else "N/A"
        
        ws.cell(row=row, column=1, value=idx).border = thin_border
        ws.cell(row=row, column=2, value=book_title).border = thin_border
        ws.cell(row=row, column=3, value=receipt.borrow_date.strftime("%d/%m/%Y %H:%M")).border = thin_border
        ws.cell(row=row, column=4, value=overdue_days).border = thin_border
        row += 1
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 15
    
    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_sach_tra_tre_{report_date.strftime("%Y_%m_%d")}.xlsx"'
    wb.save(response)
    return response


@permission_required('Báo cáo mượn sách theo thể loại', 'view')
def report_borrow_situation_view(request):
    """
    Báo cáo tình hình mượn sách theo khoảng thời gian
    """
    from datetime import timedelta
    
    # Lấy ngày từ request
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')
    
    # Mặc định: 1 năm trước đến hiện tại
    now = timezone.now()
    if from_date_str:
        try:
            from_date = timezone.datetime.strptime(from_date_str, '%Y-%m-%d')
            from_date = timezone.make_aware(from_date, timezone.get_current_timezone())
        except ValueError:
            from_date = now - timedelta(days=365)
    else:
        from_date = now - timedelta(days=365)
    
    if to_date_str:
        try:
            to_date = timezone.datetime.strptime(to_date_str, '%Y-%m-%d')
            to_date = timezone.make_aware(to_date.replace(hour=23, minute=59, second=59), timezone.get_current_timezone())
        except ValueError:
            to_date = now
    else:
        to_date = now
    
    # Lấy dữ liệu mượn trong khoảng thời gian
    borrow_receipts = BorrowReturnReceipt.objects.filter(
        borrow_date__gte=from_date,
        borrow_date__lte=to_date
    ).select_related('book_item__book__book_title__category')
    
    # Đếm theo thể loại
    category_stats = {}
    total_borrows = 0
    
    for receipt in borrow_receipts:
        if receipt.book_item and receipt.book_item.book:
            category_name = receipt.book_item.book.book_title.category.category_name
            category_stats[category_name] = category_stats.get(category_name, 0) + 1
            total_borrows += 1
    
    # Tạo dữ liệu báo cáo
    report_data = []
    for idx, (category_name, borrow_count) in enumerate(sorted(category_stats.items(), key=lambda x: -x[1]), 1):
        percentage = round((borrow_count / total_borrows * 100), 2) if total_borrows > 0 else 0
        report_data.append({
            'stt': idx,
            'category_name': category_name,
            'borrow_count': borrow_count,
            'percentage': percentage
        })
    
    # Dữ liệu cho biểu đồ (JSON)
    import json
    chart_labels = [item['category_name'] for item in report_data]
    chart_data = [item['borrow_count'] for item in report_data]
    
    context = {
        'report_data': report_data,
        'total_borrows': total_borrows,
        'from_date': from_date,
        'to_date': to_date,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'page_title': 'Báo cáo Tình hình mượn sách'
    }
    
    return render(request, 'app/reports/report_borrow_situation.html', context)


@permission_required('Báo cáo', 'view')
def report_borrow_situation_excel(request):
    """
    Export báo cáo tình hình mượn sách ra file Excel
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    from django.http import HttpResponse
    from datetime import timedelta
    
    # Lấy ngày từ request
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')
    
    now = timezone.now()
    if from_date_str:
        try:
            from_date = timezone.datetime.strptime(from_date_str, '%Y-%m-%d')
            from_date = timezone.make_aware(from_date, timezone.get_current_timezone())
        except ValueError:
            from_date = now - timedelta(days=365)
    else:
        from_date = now - timedelta(days=365)
    
    if to_date_str:
        try:
            to_date = timezone.datetime.strptime(to_date_str, '%Y-%m-%d')
            to_date = timezone.make_aware(to_date.replace(hour=23, minute=59, second=59), timezone.get_current_timezone())
        except ValueError:
            to_date = now
    else:
        to_date = now
    
    # Lấy dữ liệu
    borrow_receipts = BorrowReturnReceipt.objects.filter(
        borrow_date__gte=from_date,
        borrow_date__lte=to_date
    ).select_related('book_item__book__book_title__category')
    
    category_stats = {}
    total_borrows = 0
    
    for receipt in borrow_receipts:
        if receipt.book_item and receipt.book_item.book:
            category_name = receipt.book_item.book.book_title.category.category_name
            category_stats[category_name] = category_stats.get(category_name, 0) + 1
            total_borrows += 1
    
    # Tạo workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Tình hình mượn sách"
    
    # Style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = f'Báo cáo Tình hình mượn sách'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    ws.merge_cells('A2:D2')
    ws['A2'] = f'Từ {from_date.strftime("%d/%m/%Y")} đến {to_date.strftime("%d/%m/%Y")}'
    ws['A2'].alignment = Alignment(horizontal='center')
    
    # Headers
    headers = ['STT', 'Tên thể loại', 'Số lượt mượn', 'Tỉ lệ (%)']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
    
    # Data
    row = 5
    for idx, (category_name, borrow_count) in enumerate(sorted(category_stats.items(), key=lambda x: -x[1]), 1):
        percentage = round((borrow_count / total_borrows * 100), 2) if total_borrows > 0 else 0
        ws.cell(row=row, column=1, value=idx).border = thin_border
        ws.cell(row=row, column=2, value=category_name).border = thin_border
        ws.cell(row=row, column=3, value=borrow_count).border = thin_border
        ws.cell(row=row, column=4, value=f"{percentage}%").border = thin_border
        row += 1
    
    # Total
    ws.merge_cells(f'A{row}:B{row}')
    ws.cell(row=row, column=1, value='Tổng số lượt mượn:').font = Font(bold=True)
    ws.cell(row=row, column=3, value=total_borrows).font = Font(bold=True)
    
    # Column widths
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12
    
    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_tinh_hinh_muon_{from_date.strftime("%Y%m%d")}_{to_date.strftime("%Y%m%d")}.xlsx"'
    wb.save(response)
    return response


# ==================== SYSTEM PARAMETERS - YC8 ====================

@permission_required('Thay đổi quy định', 'view')
def parameter_update_view(request):
    """
    YC8 - Thay đổi quy định hệ thống
    
    Cho phép thay đổi:
    - Tuổi độc giả, thời hạn thẻ
    - Khoảng cách năm xuất bản
    - Số sách mượn tối đa, số ngày mượn
    - Đơn giá phạt
    - Quy định kiểm tra số tiền thu
    """
    # Lấy hoặc tạo bản ghi Parameter duy nhất
    parameter, created = Parameter.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        # Kiểm tra quyền edit cho POST request
        from .decorators import check_permission
        if not check_permission(request.user, 'Thay đổi quy định', 'edit'):
            messages.error(request, 'Bạn không có quyền sửa "Cài đặt hệ thống".')
            return redirect('parameter_update')
        
        form = ParameterForm(request.POST, instance=parameter)
        if form.is_valid():
            try:
                # Lưu các thay đổi (D4, D5)
                updated_param = form.save()
                
                messages.success(
                    request,
                    ' Cập nhật quy định thành công! '
                    f'Tuổi: {updated_param.min_age}-{updated_param.max_age}, '
                    f'Thời hạn thẻ: {updated_param.card_validity_period} tháng, '
                    f'Số sách mượn tối đa: {updated_param.max_borrowed_books}, '
                    f'Số ngày mượn tối đa: {updated_param.max_borrow_days}, '
                    f'Tiền phạt: {updated_param.fine_rate:,}đ/ngày'
                )
                return redirect('parameter_update')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        else:
            # Hiển thị lỗi validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # GET: Hiển thị form với giá trị hiện tại (D3)
        form = ParameterForm(instance=parameter)
    
    # Lấy danh sách loại độc giả với số lượng
    reader_types = ReaderType.objects.annotate(
        reader_count=Count('readers')
    ).order_by('reader_type_name')
    
    context = {
        'form': form,
        'parameter': parameter,
        'reader_types': reader_types,
        'page_title': 'Thay đổi quy định hệ thống'
    }
    
    return render(request, 'app/settings/parameter_update.html', context)


# ==================== QUẢN LÝ NGƯỜI DÙNG ====================

@permission_required('Quản lý người dùng', 'view')
def user_list_view(request):
    """
    Danh sách người dùng - Chỉ dành cho Quản lý
    Hiển thị tất cả users với vai trò của họ
    """
    users = User.objects.all().order_by('-date_joined')
    
    # Thêm thông tin vai trò cho mỗi user
    user_data = []
    for user in users:
        role = 'Quản lý' if user.is_superuser else ('Thủ thư' if user.is_staff else 'Người dùng')
        user_data.append({
            'user': user,
            'role': role,
            'is_active_text': 'Đang hoạt động' if user.is_active else 'Đã khóa'
        })
    
    context = {
        'user_data': user_data,
        'page_title': 'Quản lý người dùng'
    }
    
    return render(request, 'app/users/user_list.html', context)


@permission_required('Quản lý người dùng', 'add')
def user_create_view(request):
    """
    Tạo người dùng mới - Chỉ dành cho Quản lý
    
    Cho phép tạo:
    - Thủ thư (is_staff=True)
    - Quản lý (is_superuser=True)
    """
    from .models import LibraryUser
    from datetime import date
    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        user_group_id = request.POST.get('user_group')  # Vai trò = UserGroup
        
        # Validation
        if not username or not password:
            messages.error(request, 'Tên đăng nhập và mật khẩu là bắt buộc.')
        elif not user_group_id:
            messages.error(request, 'Vui lòng chọn vai trò.')
        elif password != password_confirm:
            messages.error(request, 'Mật khẩu xác nhận không khớp.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Tên đăng nhập "{username}" đã tồn tại.')
        elif email and User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" đã được sử dụng.')
        else:
            try:
                # Validate password strength
                # Check password with a temporary user object for similarity checks
                temp_user = User(username=username, email=email)
                validate_password(password, user=temp_user)
                
                with transaction.atomic():
                    # Lấy UserGroup đã chọn
                    user_group = UserGroup.objects.get(id=user_group_id)
                    role_name = user_group.user_group_name
                    
                    # Tạo user mới
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    # Gán vai trò dựa trên UserGroup
                    # "Quản lý" = superuser, còn lại = staff
                    if role_name == 'Quản lý':
                        user.is_staff = True
                        user.is_superuser = True
                    else:
                        user.is_staff = True
                        user.is_superuser = False
                        
                        # Tạo LibraryUser liên kết với UserGroup
                        LibraryUser.objects.create(
                            user=user,
                            full_name=f"{first_name} {last_name}".strip() or username,
                            date_of_birth=date(1990, 1, 1),
                            position=role_name,
                            user_group=user_group,
                            email=email or '',
                            is_active=True
                        )
                    
                    user.save()
                    
                    messages.success(
                        request,
                        f'Đã tạo tài khoản "{username}" với vai trò "{role_name}" thành công!'
                    )
                    return redirect('user_list')
                    
            except ValidationError as e:
                # Validation error from validate_password - Join lists into a single string
                error_msg = ' '.join(e.messages)
                messages.error(request, error_msg)
            except UserGroup.DoesNotExist:
                messages.error(request, 'Vai trò không hợp lệ.')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    
    # Lấy danh sách user groups cho dropdown
    user_groups = UserGroup.objects.all().order_by('user_group_name')
    
    context = {
        'page_title': 'Tạo người dùng mới',
        'user_groups': user_groups
    }
    
    return render(request, 'app/users/user_form.html', context)


@permission_required('Quản lý người dùng', 'edit')
def user_edit_view(request, user_id):
    """
    Chỉnh sửa thông tin người dùng - Chỉ dành cho Quản lý
    
    Cho phép:
    - Thay đổi thông tin cơ bản
    - Thay đổi vai trò (UserGroup)
    - Khóa/Mở khóa tài khoản
    - Reset mật khẩu
    """
    from .models import LibraryUser
    user = get_object_or_404(User, id=user_id)
    
    # Lấy thông tin mở rộng LibraryUser (nếu có)
    try:
        library_user = LibraryUser.objects.get(user=user)
        current_group_id = library_user.user_group.id if library_user.user_group else None
    except LibraryUser.DoesNotExist:
        library_user = None
        current_group_id = None

    if request.method == 'POST':
        action = request.POST.get('action', 'update')
        
        if action == 'update':
            email = request.POST.get('email', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            user_group_id = request.POST.get('user_group')
            is_active = request.POST.get('is_active') == 'on'
            
            # Validation email
            if email and User.objects.filter(email=email).exclude(id=user_id).exists():
                messages.error(request, f'Email "{email}" đã được sử dụng bởi tài khoản khác.')
            else:
                try:
                    with transaction.atomic():
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name
                        user.is_active = is_active
                        
                        # Cập nhật vai trò nếu có thay đổi
                        if user_group_id:
                            try:
                                user_group = UserGroup.objects.get(id=user_group_id)
                                role_name = user_group.user_group_name
                                
                                # Cập nhật User flags
                                if role_name == 'Quản lý':
                                    user.is_staff = True
                                    user.is_superuser = True
                                else:
                                    user.is_staff = True
                                    user.is_superuser = False
                                
                                # Cập nhật LibraryUser
                                if not library_user:
                                    # Nếu chưa có LibraryUser thì tạo mới
                                    from datetime import date
                                    library_user = LibraryUser.objects.create(
                                        user=user,
                                        full_name=f"{first_name} {last_name}".strip() or user.username,
                                        date_of_birth=date(1990, 1, 1), # Default
                                        position=role_name,
                                        user_group=user_group,
                                        email=email or ''
                                    )
                                else:
                                    library_user.user_group = user_group
                                    library_user.position = role_name
                                    library_user.save()
                                    
                            except UserGroup.DoesNotExist:
                                pass # Giữ nguyên nếu ID không hợp lệ
                        
                        user.save()
                        
                        messages.success(request, f'Đã cập nhật thông tin người dùng "{user.username}".')
                        return redirect('user_list')
                        
                except Exception as e:
                    messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        
        elif action == 'reset_password':
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            if not new_password:
                messages.error(request, 'Vui lòng nhập mật khẩu mới.')
            elif new_password != confirm_password:
                messages.error(request, 'Mật khẩu xác nhận không khớp.')
            else:
                try:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, f'Đã reset mật khẩu cho người dùng "{user.username}".')
                    return redirect('user_list')
                except Exception as e:
                    messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    
    # Lấy danh sách user groups
    user_groups = UserGroup.objects.all().order_by('user_group_name')
    
    # Xác định vai trò hiện tại để hiển thị nếu không tìm thấy LibraryUser
    current_role_display = 'Quản lý' if user.is_superuser else ('Thủ thư' if user.is_staff else 'Người dùng')
    if library_user and library_user.user_group:
        current_role_display = library_user.user_group.user_group_name
    
    context = {
        'edit_user': user,
        'user_groups': user_groups,
        'current_group_id': current_group_id,
        'current_role': current_role_display,
        'page_title': f'Chỉnh sửa người dùng: {user.username}'
    }
    
    return render(request, 'app/users/user_form.html', context)


@permission_required('Quản lý người dùng', 'delete')
def user_delete_view(request, user_id):
    """
    Xóa người dùng - Chỉ dành cho Quản lý
    
    Lưu ý:
    - Không thể xóa chính mình
    - Xóa vĩnh viễn (cẩn thận!)
    """
    user = get_object_or_404(User, id=user_id)
    
    # Không cho phép xóa chính mình
    if user.id == request.user.id:
        messages.error(request, 'Không thể xóa tài khoản của chính bạn!')
        return redirect('user_list')
    
    if request.method == 'POST':
        username = user.username
        try:
            user.delete()
            messages.success(request, f'Đã xóa người dùng "{username}" khỏi hệ thống.')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra khi xóa: {str(e)}')
        
        return redirect('user_list')
    
    context = {
        'delete_user': user,
        'page_title': 'Xác nhận xóa người dùng'
    }
    
    return render(request, 'app/users/user_delete_confirm.html', context)


# ==================== ĐĂNG KÝ TÀI KHOẢN ====================

def register_view(request):
    """
    Đăng ký tài khoản mới
    
    - Tài khoản mới mặc định: is_active=False (cần Quản lý kích hoạt)
    - Vai trò mặc định: Thủ thư (is_staff=True, is_superuser=False)
    - Sau khi đăng ký, hiển thị thông báo chờ duyệt
    """
    # Nếu đã đăng nhập, chuyển về trang chủ
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin bắt buộc.')
        elif password != password_confirm:
            messages.error(request, 'Mật khẩu xác nhận không khớp.')
        elif len(password) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Tên đăng nhập "{username}" đã tồn tại.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" đã được sử dụng.')
        else:
            try:
                with transaction.atomic():
                    # Tạo user mới (CHƯA KÍCH HOẠT)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=False,  # Cần Quản lý kích hoạt
                        is_staff=True,    # Mặc định là Thủ thư
                        is_superuser=False
                    )
                    
                    messages.success(
                        request,
                        f'Đăng ký tài khoản "{username}" thành công! '
                        'Vui lòng chờ quản trị viên kích hoạt tài khoản.'
                    )
                    return redirect('login')
                    
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    
    context = {
        'page_title': 'Đăng ký tài khoản'
    }
    
    return render(request, 'accounts/register.html', context)


# ==================== BOOK DETAIL & EDIT ====================

@permission_required('Quản lý kho sách', 'view')
def book_detail_view(request, book_id):
    """
    Xem chi tiết sách
    Hiển thị thông tin đầy đủ về sách và cho phép chuyển sang chỉnh sửa
    """
    book = get_object_or_404(Book, id=book_id)
    
    # Lấy thông tin về tình trạng mượn
    book_items = BookItem.objects.filter(book=book)
    borrowed_items = book_items.filter(is_borrowed=True)
    
    context = {
        'book': book,
        'book_items': book_items,
        'borrowed_count': borrowed_items.count(),
        'available_count': book_items.filter(is_borrowed=False).count(),
        'page_title': f'Chi tiết sách - {book.book_title.book_title}'
    }
    
    return render(request, 'app/books/book_detail.html', context)


@permission_required('Quản lý kho sách', 'edit')
def book_edit_view(request, book_id):
    """
    Chỉnh sửa thông tin sách
    - Admin (superuser): chỉnh sửa tất cả các trường
    - Staff: chỉ chỉnh sửa số lượng, ISBN, phiên bản, ngôn ngữ
    """
    book = get_object_or_404(Book, id=book_id)
    is_admin = request.user.is_superuser
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, instance=book, is_admin=is_admin)
        if form.is_valid():
            try:
                # Nếu là staff, chỉ lưu các trường được phép
                if not is_admin:
                    # Giữ nguyên các giá trị của trường admin-only
                    book = form.save(commit=False)
                    original = Book.objects.get(id=book_id)
                    book.unit_price = original.unit_price
                    book.publish_year = original.publish_year
                    book.publisher = original.publisher
                    book.save()
                else:
                    form.save()
                
                messages.success(request, f'Cập nhật sách "{book.book_title.book_title}" thành công!')
                return redirect('book_detail', book_id=book.id)
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = BookEditForm(instance=book, is_admin=is_admin)
    
    context = {
        'form': form,
        'book': book,
        'is_admin': is_admin,
        'page_title': f'Chỉnh sửa sách - {book.book_title.book_title}'
    }
    
    return render(request, 'app/books/book_edit.html', context)


# ==================== READER TYPE MANAGEMENT ====================

@manager_required
def reader_type_list_view(request):
    """
    Danh sách loại độc giả
    """
    reader_types = ReaderType.objects.annotate(
        reader_count=Count('readers')
    ).order_by('reader_type_name')
    
    context = {
        'reader_types': reader_types,
        'page_title': 'Quản lý loại độc giả'
    }
    
    return render(request, 'app/settings/reader_type_list.html', context)


@manager_required
def reader_type_create_view(request):
    """
    Thêm loại độc giả mới
    """
    if request.method == 'POST':
        form = ReaderTypeForm(request.POST)
        if form.is_valid():
            reader_type = form.save()
            messages.success(request, f'Đã thêm loại độc giả "{reader_type.reader_type_name}" thành công!')
            return redirect('reader_type_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ReaderTypeForm()
    
    context = {
        'form': form,
        'page_title': 'Thêm loại độc giả mới'
    }
    
    return render(request, 'app/settings/reader_type_form.html', context)


@manager_required
def reader_type_edit_view(request, reader_type_id):
    """
    Chỉnh sửa loại độc giả
    """
    reader_type = get_object_or_404(ReaderType, id=reader_type_id)
    
    if request.method == 'POST':
        form = ReaderTypeForm(request.POST, instance=reader_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật loại độc giả "{reader_type.reader_type_name}" thành công!')
            return redirect('reader_type_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ReaderTypeForm(instance=reader_type)
    
    context = {
        'form': form,
        'reader_type': reader_type,
        'page_title': f'Chỉnh sửa loại độc giả - {reader_type.reader_type_name}'
    }
    
    return render(request, 'app/settings/reader_type_form.html', context)


@manager_required
def reader_type_delete_view(request, reader_type_id):
    """
    Xóa loại độc giả
    Không cho phép xóa nếu còn độc giả thuộc loại này
    """
    reader_type = get_object_or_404(ReaderType, id=reader_type_id)
    
    # Kiểm tra có độc giả nào thuộc loại này không
    reader_count = Reader.objects.filter(reader_type=reader_type).count()
    
    if request.method == 'POST':
        if reader_count > 0:
            messages.error(
                request, 
                f'Không thể xóa loại độc giả "{reader_type.reader_type_name}" vì còn {reader_count} độc giả thuộc loại này.'
            )
        else:
            name = reader_type.reader_type_name
            reader_type.delete()
            messages.success(request, f'Đã xóa loại độc giả "{name}" thành công!')
        return redirect('reader_type_list')
    
    context = {
        'reader_type': reader_type,
        'reader_count': reader_count,
        'page_title': f'Xóa loại độc giả - {reader_type.reader_type_name}'
    }
    
    return render(request, 'app/settings/reader_type_delete.html', context)


# ==================== PERMISSION MANAGEMENT VIEWS ====================

@permission_required('Quản lý quyền', 'view')
def user_group_list_view(request):
    """Danh sách nhóm người dùng"""
    user_groups = UserGroup.objects.all().order_by('user_group_name')
    
    context = {
        'user_groups': user_groups,
        'page_title': 'Quản lý nhóm người dùng'
    }
    return render(request, 'app/permissions/user_group_list.html', context)


@permission_required('Quản lý quyền', 'add')
def user_group_create_view(request):
    """Tạo nhóm người dùng mới"""
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            user_group = form.save()
            messages.success(request, f'Đã tạo nhóm "{user_group.user_group_name}" thành công!')
            return redirect('user_group_list')
    else:
        form = UserGroupForm()
    
    context = {
        'form': form,
        'page_title': 'Thêm nhóm người dùng',
        'is_edit': False
    }
    return render(request, 'app/permissions/user_group_form.html', context)


@permission_required('Quản lý quyền', 'edit')
def user_group_edit_view(request, group_id):
    """Sửa nhóm người dùng"""
    user_group = get_object_or_404(UserGroup, id=group_id)
    
    if request.method == 'POST':
        form = UserGroupForm(request.POST, instance=user_group)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật nhóm "{user_group.user_group_name}" thành công!')
            return redirect('user_group_list')
    else:
        form = UserGroupForm(instance=user_group)
    
    context = {
        'form': form,
        'user_group': user_group,
        'page_title': f'Sửa nhóm - {user_group.user_group_name}',
        'is_edit': True
    }
    return render(request, 'app/permissions/user_group_form.html', context)


@permission_required('Quản lý quyền', 'delete')
def user_group_delete_view(request, group_id):
    """Xóa nhóm người dùng"""
    user_group = get_object_or_404(UserGroup, id=group_id)
    
    # Đếm số user thuộc nhóm này
    from .models import LibraryUser
    user_count = LibraryUser.objects.filter(user_group=user_group).count()
    
    if request.method == 'POST':
        if user_count > 0:
            messages.error(request, f'Không thể xóa nhóm "{user_group.user_group_name}" vì còn {user_count} người dùng!')
        else:
            name = user_group.user_group_name
            user_group.delete()
            messages.success(request, f'Đã xóa nhóm "{name}" thành công!')
        return redirect('user_group_list')
    
    context = {
        'user_group': user_group,
        'user_count': user_count,
        'page_title': f'Xóa nhóm - {user_group.user_group_name}'
    }
    return render(request, 'app/permissions/user_group_delete.html', context)


@permission_required('Quản lý quyền', 'view')
def function_list_view(request):
    """Danh sách chức năng"""
    functions = Function.objects.all().order_by('function_name')
    
    context = {
        'functions': functions,
        'page_title': 'Quản lý chức năng hệ thống'
    }
    return render(request, 'app/permissions/function_list.html', context)


@permission_required('Quản lý quyền', 'add')
def function_create_view(request):
    """Tạo chức năng mới"""
    if request.method == 'POST':
        form = FunctionForm(request.POST)
        if form.is_valid():
            function = form.save()
            messages.success(request, f'Đã tạo chức năng "{function.function_name}" thành công!')
            return redirect('function_list')
    else:
        form = FunctionForm()
    
    context = {
        'form': form,
        'page_title': 'Thêm chức năng',
        'is_edit': False
    }
    return render(request, 'app/permissions/function_form.html', context)


@permission_required('Quản lý quyền', 'edit')
def function_edit_view(request, function_id):
    """Sửa chức năng"""
    function = get_object_or_404(Function, id=function_id)
    
    if request.method == 'POST':
        form = FunctionForm(request.POST, instance=function)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật chức năng "{function.function_name}" thành công!')
            return redirect('function_list')
    else:
        form = FunctionForm(instance=function)
    
    context = {
        'form': form,
        'function': function,
        'page_title': f'Sửa chức năng - {function.function_name}',
        'is_edit': True
    }
    return render(request, 'app/permissions/function_form.html', context)


@permission_required('Quản lý quyền', 'delete')
def function_delete_view(request, function_id):
    """Xóa chức năng"""
    function = get_object_or_404(Function, id=function_id)
    
    # Đếm số permission liên quan
    permission_count = Permission.objects.filter(function=function).count()
    
    if request.method == 'POST':
        name = function.function_name
        function.delete()
        messages.success(request, f'Đã xóa chức năng "{name}" thành công!')
        return redirect('function_list')
    
    context = {
        'function': function,
        'permission_count': permission_count,
        'page_title': f'Xóa chức năng - {function.function_name}'
    }
    return render(request, 'app/permissions/function_delete.html', context)


@permission_required('Quản lý quyền', 'edit')
def permission_matrix_view(request, group_id):
    """Quản lý quyền cho nhóm người dùng (ma trận quyền)"""
    user_group = get_object_or_404(UserGroup, id=group_id)
    functions = Function.objects.all().order_by('function_name')
    
    if request.method == 'POST':
        # Xử lý cập nhật quyền
        for function in functions:
            can_view = request.POST.get(f'view_{function.id}') == 'on'
            can_add = request.POST.get(f'add_{function.id}') == 'on'
            can_edit = request.POST.get(f'edit_{function.id}') == 'on'
            can_delete = request.POST.get(f'delete_{function.id}') == 'on'
            
            # Cập nhật hoặc tạo mới permission
            permission, created = Permission.objects.update_or_create(
                user_group=user_group,
                function=function,
                defaults={
                    'can_view': can_view,
                    'can_add': can_add,
                    'can_edit': can_edit,
                    'can_delete': can_delete
                }
            )
        
        messages.success(request, f'Đã cập nhật quyền cho nhóm "{user_group.user_group_name}" thành công!')
        return redirect('permission_matrix', group_id=group_id)
    
    # Lấy quyền hiện tại
    permissions = {}
    for p in Permission.objects.filter(user_group=user_group):
        permissions[str(p.function_id)] = {
            'can_view': p.can_view,
            'can_add': p.can_add,
            'can_edit': p.can_edit,
            'can_delete': p.can_delete
        }
    
    import json
    context = {
        'user_group': user_group,
        'functions': functions,
        'permissions': json.dumps(permissions),
        'page_title': f'Phân quyền - {user_group.user_group_name}'
    }
    return render(request, 'app/permissions/permission_matrix.html', context)

