from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Reader, ReaderType, Parameter, BookTitle, Category, Author, BookImportReceipt, BookImportDetail, Book, BookItem, BorrowReturnReceipt, Receipt


class SafeIntegerField(forms.IntegerField):
    """Custom IntegerField that defaults to min_value if value is less"""
    
    def __init__(self, min_value=None, *args, **kwargs):
        # Lưu min_value trước khi gọi super
        self.min_value_default = min_value
        # Gọi super với min_value để kích hoạt validation
        super().__init__(min_value=min_value, *args, **kwargs)
    
    def to_python(self, value):
        """Convert to python int, default to min_value if needed"""
        if value in self.empty_values:
            if self.min_value_default is not None:
                return self.min_value_default
            return None
        
        try:
            value_int = int(value)
            # Nếu giá trị < min_value_default, auto-set về min_value
            if self.min_value_default is not None and value_int < self.min_value_default:
                return self.min_value_default
            return value_int
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')


class LibraryLoginForm(AuthenticationForm):
    """
    Form đăng nhập cho hệ thống thư viện
    Sử dụng Django User (superuser/staff)
    """
    username = forms.CharField(
        label='Tên đăng nhập',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên đăng nhập',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu'
        })
    )
    
    error_messages = {
        'invalid_login': 'Tên đăng nhập hoặc mật khẩu không đúng.',
        'inactive': 'Tài khoản này đã bị vô hiệu hóa.',
    }


class ReaderForm(forms.ModelForm):
    """
    Form lập thẻ độc giả - YC1
    Validate theo QĐ1: tuổi từ min_age đến max_age, loại độc giả hợp lệ
    """
    
    class Meta:
        model = Reader
        fields = [
            'reader_name',
            'reader_type',
            'date_of_birth',
            'address',
            'email',
            'card_creation_date'
        ]
        widgets = {
            'reader_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ và tên'
            }),
            'reader_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nhập địa chỉ'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'card_creation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'reader_name': 'Họ và tên',
            'reader_type': 'Loại độc giả',
            'date_of_birth': 'Ngày sinh',
            'address': 'Địa chỉ',
            'email': 'Email',
            'card_creation_date': 'Ngày lập thẻ'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set ngày lập thẻ mặc định là hôm nay
        if not self.instance.pk:
            from django.utils import timezone
            self.initial['card_creation_date'] = timezone.now().date()
    
    def validate_reader_data(self):
        """Kiểm tra toàn bộ dữ liệu lập thẻ độc giả theo QĐ1"""
        cleaned_data = super().clean()
        
        # Kiểm tra loại độc giả
        reader_type = cleaned_data.get('reader_type')
        if not reader_type:
            raise ValidationError({
                'reader_type': "Vui lòng chọn loại độc giả."
            })
        
        # Kiểm tra ngày sinh và tuổi
        dob = cleaned_data.get('date_of_birth')
        if not dob:
            raise ValidationError({
                'date_of_birth': "Vui lòng nhập ngày sinh."
            })
        
        # Tính tuổi
        from datetime import date
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        # Lấy tham số hệ thống
        try:
            params = Parameter.objects.first()
            if not params:
                raise ValidationError("Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.")
            
            # Kiểm tra tuổi tối thiểu
            if age < params.min_age:
                raise ValidationError({
                    'date_of_birth': (
                        f"Độc giả phải từ {params.min_age} tuổi trở lên. "
                        f"Tuổi hiện tại: {age} tuổi."
                    )
                })
            
            # Kiểm tra tuổi tối đa
            if age > params.max_age:
                raise ValidationError({
                    'date_of_birth': (
                        f"Độc giả không được quá {params.max_age} tuổi. "
                        f"Tuổi hiện tại: {age} tuổi."
                    )
                })
        except Parameter.DoesNotExist:
            raise ValidationError("Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.")
        
        # Kiểm tra email trùng lặp
        email = cleaned_data.get('email')
        if email:
            existing = Reader.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError({
                    'email': 'Email này đã được đăng ký bởi độc giả khác.'
                })
        
        return cleaned_data
    
    def clean(self):
        """Gọi hàm kiểm tra dữ liệu lập thẻ độc giả"""
        return self.validate_reader_data()


class BorrowBookForm(forms.Form):
    """
    Form cho mượn sách - YC4
    Validate theo QĐ4: thẻ còn hạn, không quá hạn, sách chưa mượn, không quá 5 quyển
    Hỗ trợ mượn nhiều sách cùng lúc (miễn không vượt giới hạn)
    """
    
    reader_id = forms.IntegerField(
        label='Chọn độc giả',
        widget=forms.HiddenInput()
    )
    
    book_id = forms.CharField(
        label='Chọn sách',
        widget=forms.HiddenInput()  # Sẽ nhận "id1,id2,id3"
    )
    
    borrow_date = forms.DateField(
        label='Ngày mượn',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def validate_borrow_data(self):
        """Kiểm tra dữ liệu cho mượn sách theo QĐ4"""
        cleaned_data = super().clean()
        
        reader_id = cleaned_data.get('reader_id')
        book_ids_str = cleaned_data.get('book_id', '')
        borrow_date = cleaned_data.get('borrow_date')
        
        # Parse book_ids từ string
        try:
            book_ids = [int(bid.strip()) for bid in book_ids_str.split(',') if bid.strip()]
        except ValueError:
            raise ValidationError({'book_id': 'Sách không hợp lệ.'})
        
        if not book_ids:
            raise ValidationError({'book_id': 'Vui lòng chọn ít nhất 1 quyển sách.'})
        
        # Lấy tham số hệ thống
        try:
            params = Parameter.objects.first()
            if not params:
                raise ValidationError("Hệ thống chưa được cấu hình.")
        except Parameter.DoesNotExist:
            raise ValidationError("Hệ thống chưa được cấu hình.")
        
        # Kiểm tra độc giả tồn tại
        try:
            reader = Reader.objects.get(id=reader_id)
        except Reader.DoesNotExist:
            raise ValidationError({
                'reader_id': 'Độc giả không tồn tại.'
            })
        
        # QĐ4.1: Kiểm tra thẻ còn hạn
        from datetime import date, datetime
        today = date.today()
        if reader.expiration_date and reader.expiration_date.date() < today:
            raise ValidationError({
                'reader_id': f'Thẻ độc giả đã hết hạn (hết hạn: {reader.expiration_date.strftime("%d/%m/%Y")}).'
            })
        
        # QĐ4.2: Kiểm tra độc giả không có sách mượn quá hạn
        overdue_borrows = BorrowReturnReceipt.objects.filter(
            reader=reader,
            return_date__isnull=True,
            due_date__lt=today
        ).exists()
        if overdue_borrows:
            raise ValidationError({
                'reader_id': 'Độc giả có sách mượn quá hạn. Vui lòng trả sách trước khi mượn thêm.'
            })
        
        # QĐ4.4: Kiểm tra số sách đang mượn + số sách chọn không vượt quá tối đa
        current_borrowed = BorrowReturnReceipt.objects.filter(
            reader=reader,
            return_date__isnull=True
        ).count()
        
        total_will_borrow = current_borrowed + len(book_ids)
        if total_will_borrow > params.max_borrowed_books:
            raise ValidationError({
                'reader_id': f'Độc giả đang mượn {current_borrowed} quyển. Chỉ có thể mượn thêm {params.max_borrowed_books - current_borrowed} quyển nữa (tối đa {params.max_borrowed_books}).'
            })
        
        # Kiểm tra tất cả sách tồn tại và có sách còn sẵn
        books = {}
        for book_id in book_ids:
            try:
                book = Book.objects.get(id=book_id)
                books[book_id] = book
            except Book.DoesNotExist:
                raise ValidationError({
                    'book_id': f'Sách (ID: {book_id}) không tồn tại.'
                })
            
            # QĐ4.3: Kiểm tra sách không đang được mượn (còn sách có sẵn)
            available_items = BookItem.objects.filter(book=book, is_borrowed=False).exists()
            if not available_items:
                raise ValidationError({
                    'book_id': f'Sách "{book.book_title.book_title}" hiện đang không có sẵn (tất cả đang được mượn).'
                })
        
        # Lưu lại book_ids đã parse
        cleaned_data['book_ids'] = book_ids
        cleaned_data['books'] = books
        
        return cleaned_data
    
    def clean(self):
        """Gọi hàm kiểm tra dữ liệu cho mượn sách"""
        return self.validate_borrow_data()


class BookSearchForm(forms.Form):
    """
    Form tra cứu sách - YC3
    Cho phép tìm kiếm theo tên sách, thể loại, tác giả, ...
    """
    
    search_text = forms.CharField(
        label='Tìm kiếm theo tên sách hoặc mã sách',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên sách hoặc mã sách...'
        })
    )
    
    category = forms.ModelChoiceField(
        label='Thể loại',
        queryset=Category.objects.all(),
        empty_label='-- Tất cả thể loại --',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    author = forms.ModelChoiceField(
        label='Tác giả',
        queryset=Author.objects.all(),
        empty_label='-- Tất cả tác giả --',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    status = forms.ChoiceField(
        label='Tình trạng',
        choices=[
            ('', '-- Tất cả tình trạng --'),
            ('available', 'Còn sách'),
            ('unavailable', 'Hết sách'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class BookEditForm(forms.ModelForm):
    """
    Form chỉnh sửa sách
    - Staff: chỉ chỉnh sửa quantity, remaining_quantity
    - Admin: chỉnh sửa tất cả các trường
    """
    
    class Meta:
        model = Book
        fields = [
            'quantity', 'remaining_quantity',
            'isbn', 'edition', 'language',
            'unit_price', 'publish_year', 'publisher'
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'remaining_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: 978-3-16-148410-0'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: Lần thứ 2'
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000'
            }),
            'publish_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': '2100'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'quantity': 'Số lượng tổng',
            'remaining_quantity': 'Số lượng còn lại',
            'isbn': 'ISBN',
            'edition': 'Phiên bản',
            'language': 'Ngôn ngữ',
            'unit_price': 'Đơn giá (VNĐ)',
            'publish_year': 'Năm xuất bản',
            'publisher': 'Nhà xuất bản',
        }
    
    def __init__(self, *args, is_admin=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_admin = is_admin
        
        # Staff chỉ được chỉnh sửa một số trường
        if not is_admin:
            # Disable các trường admin-only
            admin_only_fields = ['unit_price', 'publish_year', 'publisher']
            for field_name in admin_only_fields:
                if field_name in self.fields:
                    self.fields[field_name].widget.attrs['readonly'] = True
                    self.fields[field_name].widget.attrs['class'] += ' bg-gray-100'
    
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        remaining_quantity = cleaned_data.get('remaining_quantity')
        
        if quantity is not None and remaining_quantity is not None:
            if remaining_quantity > quantity:
                raise ValidationError({
                    'remaining_quantity': 'Số lượng còn lại không thể lớn hơn tổng số lượng'
                })
        
        return cleaned_data


class ReaderTypeForm(forms.ModelForm):
    """
    Form quản lý loại độc giả
    Dùng cho thêm/sửa ReaderType
    """
    
    class Meta:
        model = ReaderType
        fields = ['reader_type_name', 'description']
        widgets = {
            'reader_type_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên loại độc giả'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nhập mô tả (tùy chọn)'
            }),
        }
        labels = {
            'reader_type_name': 'Tên loại độc giả',
            'description': 'Mô tả',
        }
    
    def clean_reader_type_name(self):
        name = self.cleaned_data.get('reader_type_name')
        if name:
            # Check for duplicate (excluding current instance)
            existing = ReaderType.objects.filter(reader_type_name__iexact=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Loại độc giả với tên này đã tồn tại')
        return name


class BookImportForm(forms.Form):
    """
    Form tiếp nhận sách mới - YC2
    Validate theo QĐ2: Chỉ nhận sách xuất bản trong vòng 8 năm, 
    thể loại và tác giả phải hợp lệ
    """
    
    # Thông tin sách
    book_title = forms.CharField(
        label='Tên sách',
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập tên sách'
        })
    )
    
    category = forms.ModelChoiceField(
        label='Thể loại',
        queryset=Category.objects.all(),
        empty_label='-- Chọn thể loại --',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    authors = forms.ModelMultipleChoiceField(
        label='Tác giả (có thể chọn nhiều)',
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    
    publish_year = forms.IntegerField(
        label='Năm xuất bản',
        initial=2025,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'value': '2025'
        })
    )
    
    publisher = forms.CharField(
        label='Nhà xuất bản',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập nhà xuất bản'
        })
    )
    
    isbn = forms.CharField(
        label='ISBN (tùy chọn)',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: 978-3-16-148410-0'
        })
    )
    
    edition = forms.CharField(
        label='Phiên bản (tùy chọn)',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VD: Lần thứ 2, 2023'
        })
    )
    
    language = forms.CharField(
        label='Ngôn ngữ',
        max_length=50,
        initial='Tiếng Việt',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Thông tin nhập kho
    quantity = SafeIntegerField(
        label='Số lượng nhập',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '1',
            'value': '1'
        })
    )
    
    unit_price = SafeIntegerField(
        label='Đơn giá (VNĐ)',
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0',
            'value': '0'
        })
    )
    
    import_date = forms.DateField(
        label='Ngày nhập',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    description = forms.CharField(
        label='Mô tả (tùy chọn)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Nhập thông tin mô tả thêm về sách'
        })
    )
    
    notes = forms.CharField(
        label='Ghi chú (tùy chọn)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Nhập ghi chú bổ sung'
        })
    )
    
    def validate_book_import_data(self):
        """Kiểm tra toàn bộ dữ liệu nhập sách theo QĐ2"""
        cleaned_data = super().clean()
        
        # Lấy tham số hệ thống
        try:
            params = Parameter.objects.first()
            if not params:
                raise ValidationError("Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.")
        except Parameter.DoesNotExist:
            raise ValidationError("Hệ thống chưa được cấu hình. Vui lòng liên hệ quản trị viên.")
        
        # Kiểm tra số lượng
        quantity = cleaned_data.get('quantity')
        if quantity is None or quantity == '':
            raise ValidationError({
                'quantity': "Vui lòng nhập số lượng"
            })
        if isinstance(quantity, str):
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                raise ValidationError({
                    'quantity': "Số lượng phải là số nguyên"
                })
        if quantity < 1:
            raise ValidationError({
                'quantity': "Số lượng phải lớn hơn 0 (tối thiểu 1 cuốn)"
            })
        cleaned_data['quantity'] = quantity
        
        # Kiểm tra giá
        unit_price = cleaned_data.get('unit_price')
        if unit_price is None or unit_price == '' or unit_price < 0:
            cleaned_data['unit_price'] = 0
        
        # Kiểm tra năm xuất bản
        publish_year = cleaned_data.get('publish_year')
        if publish_year is None or publish_year == '':
            from datetime import date
            publish_year = date.today().year
        else:
            try:
                publish_year = int(publish_year)
            except (ValueError, TypeError):
                raise ValidationError({
                    'publish_year': "Năm xuất bản phải là số nguyên"
                })
        
        from datetime import date
        current_year = date.today().year
        
        if publish_year < 1900:
            raise ValidationError({
                'publish_year': "Năm xuất bản không được nhỏ hơn 1900"
            })
        if publish_year > current_year:
            raise ValidationError({
                'publish_year': "Năm xuất bản không được lớn hơn năm hiện tại"
            })
        
        min_year = current_year - params.book_return_period
        if publish_year < min_year:
            raise ValidationError({
                'publish_year': f'Chỉ nhận sách xuất bản từ năm {min_year} trở đi (QĐ2)'
            })
        cleaned_data['publish_year'] = publish_year
        
        # Kiểm tra tác giả
        authors = cleaned_data.get('authors')
        if not authors:
            raise ValidationError({
                'authors': 'Vui lòng chọn ít nhất 1 tác giả'
            })
        
        # Kiểm tra thể loại
        category = cleaned_data.get('category')
        if not category:
            raise ValidationError({
                'category': 'Vui lòng chọn thể loại'
            })
        
        return cleaned_data
    
    def clean(self):
        """Gọi hàm kiểm tra dữ liệu nhập sách"""
        return self.validate_book_import_data()


class ReturnBookForm(forms.Form):
    """
    Form trả sách - YC5 (redesigned)
    Chọn độc giả → chọn sách mượn → nhập ngày trả
    """
    reader_id = forms.IntegerField(widget=forms.HiddenInput())
    book_item_ids = forms.CharField(widget=forms.HiddenInput())  # JSON array
    return_date = forms.DateTimeField(
        label='Ngày trả',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'placeholder': 'Chọn ngày giờ trả sách'
        }),
        help_text='Ngày và giờ thực tế trả sách'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_reader_id(self):
        """Kiểm tra độc giả tồn tại"""
        reader_id = self.cleaned_data.get('reader_id')
        
        try:
            reader = Reader.objects.get(id=reader_id)
        except Reader.DoesNotExist:
            raise ValidationError('Độc giả không tồn tại')
        
        return reader_id
    
    def clean_book_item_ids(self):
        """Kiểm tra danh sách sách hợp lệ"""
        import json
        book_item_ids_str = self.cleaned_data.get('book_item_ids')
        
        if not book_item_ids_str:
            raise ValidationError('Vui lòng chọn ít nhất 1 quyển sách')
        
        try:
            book_item_ids = json.loads(book_item_ids_str)
            if not isinstance(book_item_ids, list) or len(book_item_ids) == 0:
                raise ValidationError('Danh sách sách không hợp lệ')
        except json.JSONDecodeError:
            raise ValidationError('Dữ liệu sách không hợp lệ')
        
        return book_item_ids_str
    
    def clean_return_date(self):
        """Kiểm tra ngày trả hợp lệ"""
        return_date = self.cleaned_data.get('return_date')
        
        if return_date and return_date.date() > timezone.now().date():
            raise ValidationError('Ngày trả không được trong tương lai')
        
        return return_date
    
    def save(self):
        """Lưu thông tin trả sách cho nhiều phiếu"""
        import json
        from django.utils import timezone
        
        reader_id = self.cleaned_data['reader_id']
        book_item_ids = json.loads(self.cleaned_data['book_item_ids'])
        return_date = self.cleaned_data['return_date']
        
        receipts_updated = []
        try:
            reader = Reader.objects.get(id=reader_id)
            
            # Cập nhật return_date cho các phiếu mượn
            receipts = BorrowReturnReceipt.objects.filter(
                reader=reader,
                book_item_id__in=book_item_ids,
                return_date__isnull=True
            )
            
            for receipt in receipts:
                receipt.return_date = return_date
                receipt.save()
                receipts_updated.append(receipt)
                
            return receipts_updated if receipts_updated else None
        except Reader.DoesNotExist:
            return None


class ReceiptForm(forms.Form):
    """
    Form lập phiếu thu tiền phạt - YC6
    Validate theo QĐ6: Số tiền thu không được vượt quá tổng nợ
    """
    reader_id = forms.IntegerField(
        label='Chọn độc giả',
        widget=forms.HiddenInput()
    )
    
    collected_amount = forms.IntegerField(
        label='Số tiền thu (VNĐ)',
        validators=[],  # Will validate in clean()
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0',
            'step': '1000',
            'placeholder': 'Nhập số tiền thu (đơn vị: đồng)'
        })
    )
    
    payment_method = forms.ChoiceField(
        label='Phương thức thanh toán',
        choices=[
            ('Tiền mặt', 'Tiền mặt'),
            ('Chuyển khoản', 'Chuyển khoản'),
            ('Thẻ', 'Thẻ'),
        ],
        initial='Tiền mặt',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    notes = forms.CharField(
        label='Ghi chú (tùy chọn)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Nhập ghi chú bổ sung'
        })
    )
    
    def clean_reader_id(self):
        """Kiểm tra độc giả tồn tại"""
        reader_id = self.cleaned_data.get('reader_id')
        
        try:
            reader = Reader.objects.get(id=reader_id)
        except Reader.DoesNotExist:
            raise ValidationError('Độc giả không tồn tại')
        
        return reader_id
    
    def clean_collected_amount(self):
        """Kiểm tra số tiền thu hợp lệ"""
        collected_amount = self.cleaned_data.get('collected_amount')
        
        if collected_amount is None or collected_amount < 0:
            raise ValidationError('Số tiền thu phải là số dương')
        
        if collected_amount == 0:
            raise ValidationError('Vui lòng nhập số tiền thu')
        
        return collected_amount
    
    def clean(self):
        """Kiểm tra theo QĐ6: số tiền không được vượt quá nợ"""
        cleaned_data = super().clean()
        
        reader_id = cleaned_data.get('reader_id')
        collected_amount = cleaned_data.get('collected_amount')
        
        if not reader_id or collected_amount is None:
            return cleaned_data
        
        try:
            reader = Reader.objects.get(id=reader_id)
            
            # QĐ6: Kiểm tra số tiền thu không được vượt quá tổng nợ
            if collected_amount > reader.total_debt:
                raise ValidationError({
                    'collected_amount': (
                        f'Số tiền thu không được vượt quá tổng nợ hiện tại ({reader.total_debt:,}đ). '
                        f'Bạn nhập: {collected_amount:,}đ'
                    )
                })
            
            if reader.total_debt == 0:
                raise ValidationError({
                    'collected_amount': 'Độc giả này không có nợ tiền phạt'
                })
        except Reader.DoesNotExist:
            raise ValidationError('Độc giả không tồn tại')
        
        return cleaned_data
    
    def save(self):
        """Lưu phiếu thu tiền và cập nhật nợ của độc giả"""
        try:
            reader = Reader.objects.get(id=self.cleaned_data['reader_id'])
            collected_amount = self.cleaned_data['collected_amount']
            payment_method = self.cleaned_data['payment_method']
            notes = self.cleaned_data.get('notes', '')
            
            # Tạo phiếu thu
            receipt = Receipt.objects.create(
                reader=reader,
                collected_amount=collected_amount,
                payment_method=payment_method,
                notes=notes
            )
            
            return receipt
        except Reader.DoesNotExist:
            return None


# ==================== PARAMETER FORM - YC8 ====================

class ParameterForm(forms.ModelForm):
    """
    Form thay đổi các tham số hệ thống - YC8
    
    Bao gồm:
    - QĐ1: Tuổi độc giả, thời hạn thẻ
    - QĐ2: Khoảng cách năm xuất bản
    - QĐ4: Số sách mượn tối đa, số ngày mượn
    - QĐ5: Đơn giá phạt
    - QĐ6: Quy định kiểm tra số tiền thu
    """
    
    class Meta:
        model = Parameter
        fields = [
            'min_age', 'max_age', 'card_validity_period',
            'book_return_period', 
            'max_borrowed_books', 'max_borrow_days',
            'fine_rate',
            'enable_receipt_amount_validation'
        ]
        widgets = {
            'min_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Tuổi tối thiểu'
            }),
            'max_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Tuổi tối đa'
            }),
            'card_validity_period': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Số tháng'
            }),
            'book_return_period': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Số năm'
            }),
            'max_borrowed_books': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Số sách'
            }),
            'max_borrow_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Số ngày'
            }),
            'fine_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
                'placeholder': 'VNĐ/ngày'
            }),
            'enable_receipt_amount_validation': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')
        
        # Kiểm tra min_age < max_age
        if min_age and max_age and min_age >= max_age:
            raise ValidationError('Tuổi tối thiểu phải nhỏ hơn tuổi tối đa')
        
        return cleaned_data


# ==================== PERMISSION MANAGEMENT FORMS ====================

from .models import UserGroup, Function, Permission


class UserGroupForm(forms.ModelForm):
    """Form for UserGroup management"""
    
    class Meta:
        model = UserGroup
        fields = ['user_group_name', 'description']
        widgets = {
            'user_group_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Nhập tên nhóm người dùng'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Mô tả nhóm người dùng'
            })
        }
        labels = {
            'user_group_name': 'Tên nhóm',
            'description': 'Mô tả'
        }


class FunctionForm(forms.ModelForm):
    """Form for Function management"""
    
    class Meta:
        model = Function
        fields = ['function_name', 'screen_name', 'url_pattern', 'description']
        widgets = {
            'function_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'VD: Quản lý sách'
            }),
            'screen_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'VD: Danh sách sách'
            }),
            'url_pattern': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'VD: /books/'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Mô tả chức năng'
            })
        }
        labels = {
            'function_name': 'Tên chức năng',
            'screen_name': 'Tên màn hình',
            'url_pattern': 'URL pattern',
            'description': 'Mô tả'
        }