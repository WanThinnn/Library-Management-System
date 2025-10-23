from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# ==================== SYSTEM PARAMETERS ====================

class Parameter(models.Model):
    """
    Bảng PARAMETER - Lưu trữ các tham số cấu hình của hệ thống
    """
    # Độ tuổi
    max_age = models.PositiveSmallIntegerField(
        verbose_name='Độ tuổi thấp nhất',
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    min_age = models.PositiveSmallIntegerField(
        verbose_name='Độ tuổi cao nhất',
        default=55,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    
    # Thời hạn thẻ
    card_validity_period = models.PositiveIntegerField(
        verbose_name='Thời hạn thẻ (tháng)',
        default=6,
        validators=[MinValueValidator(1)]
    )
    
    # Quy định về sách
    book_return_period = models.PositiveIntegerField(
        verbose_name='Nhận sách xuất bản trong vòng (năm)',
        default=8,
        validators=[MinValueValidator(1)]
    )
    max_borrowed_books = models.PositiveIntegerField(
        verbose_name='Số sách tối đa được mượn',
        default=5,
        validators=[MinValueValidator(1)]
    )
    max_borrow_days = models.PositiveIntegerField(
        verbose_name='Số ngày mượn sách tối đa',
        default=4,
        validators=[MinValueValidator(1)]
    )
    
    # Tiền phạt
    fine_rate = models.PositiveIntegerField(
        verbose_name='Đơn giá tiền phạt (VNĐ/ngày)',
        default=1000,
        validators=[MinValueValidator(0)]
    )
    
    # Quy định khác
    enable_receipt_amount_validation = models.BooleanField(
        verbose_name='Kiểm tra số tiền thu không vượt quá nợ',
        default=True
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parameter'
        verbose_name = 'Tham số hệ thống'
        verbose_name_plural = 'Tham số hệ thống'
    
    def __str__(self):
        return f"Tham số hệ thống (cập nhật: {self.updated_at.strftime('%d/%m/%Y')})"
    
    def save(self, *args, **kwargs):
        # Đảm bảo chỉ có 1 bản ghi duy nhất
        if not self.pk and Parameter.objects.exists():
            # Nếu đã tồn tại bản ghi, update thay vì tạo mới
            existing = Parameter.objects.first()
            if existing:
                self.pk = existing.pk
        super().save(*args, **kwargs)


class ReaderType(models.Model):
    """
    Bảng READER_TYPE - Loại độc giả
    """
    reader_type_name = models.CharField(
        max_length=100,
        verbose_name='Tên loại độc giả',
        unique=True
    )
    description = models.TextField(
        verbose_name='Mô tả',
        blank=True,
        null=True
    )
    
    class Meta:
        db_table = 'reader_type'
        verbose_name = 'Loại độc giả'
        verbose_name_plural = 'Loại độc giả'
        ordering = ['reader_type_name']
    
    def __str__(self):
        return self.reader_type_name


class Reader(models.Model):
    """
    Bảng READER - Thông tin độc giả
    """
    reader_name = models.CharField(
        max_length=255,
        verbose_name='Tên độc giả'
    )
    reader_type = models.ForeignKey(
        ReaderType,
        on_delete=models.PROTECT,
        verbose_name='Loại độc giả',
        related_name='readers'
    )
    date_of_birth = models.DateField(
        verbose_name='Ngày sinh'
    )
    address = models.TextField(
        verbose_name='Địa chỉ'
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Số điện thoại',
        blank=True,
        null=True
    )
    
    # Thông tin thẻ
    card_creation_date = models.DateTimeField(
        verbose_name='Ngày lập thẻ',
        default=timezone.now
    )
    expiration_date = models.DateTimeField(
        verbose_name='Ngày hết hạn thẻ'
    )
    
    # Thông tin nợ
    total_debt = models.PositiveIntegerField(
        verbose_name='Tổng nợ (VNĐ)',
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Trạng thái
    is_active = models.BooleanField(
        verbose_name='Đang hoạt động',
        default=True
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reader'
        verbose_name = 'Độc giả'
        verbose_name_plural = 'Độc giả'
        ordering = ['-card_creation_date']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['reader_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.reader_name} - {self.email}"
    
    @property
    def age(self):
        """Tính tuổi của độc giả"""
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def is_card_expired(self):
        """Kiểm tra thẻ đã hết hạn chưa"""
        return timezone.now() > self.expiration_date
    
    @property
    def days_until_expiration(self):
        """Số ngày còn lại đến khi hết hạn thẻ"""
        if self.is_card_expired:
            return 0
        delta = self.expiration_date - timezone.now()
        return delta.days
    
    def clean(self):
        """
        Validate business rules cho độc giả theo QĐ1
        """
        from django.core.exceptions import ValidationError
        
        # Kiểm tra ngày sinh trước
        # if not self.date_of_birth:
        #     raise ValidationError({"date_of_birth": "Ngày sinh không được để trống"})
        
        # Lấy tham số hệ thống
        try:
            params = Parameter.objects.first()
            if not params:
                raise ValidationError("Chưa cấu hình tham số hệ thống!")
            
            # Kiểm tra tuổi
            reader_age = self.age
            if reader_age is None:
                raise ValidationError({"date_of_birth": "Ngày sinh không hợp lệ"})
                
            if reader_age < params.min_age:
                raise ValidationError(
                    f"Độc giả phải từ {params.min_age} tuổi trở lên. Tuổi hiện tại: {reader_age}"
                )
            
            if reader_age > params.max_age:
                raise ValidationError(
                    f"Độc giả không được quá {params.max_age} tuổi. Tuổi hiện tại: {reader_age}"
                )
        except Parameter.DoesNotExist:
            raise ValidationError("Chưa cấu hình tham số hệ thống!")
    
    def save(self, *args, **kwargs):
        # Tự động tính ngày hết hạn nếu chưa có (trước khi validate)
        if not self.expiration_date:
            from dateutil.relativedelta import relativedelta
            try:
                params = Parameter.objects.first()
                months = params.card_validity_period if params else 6
            except:
                months = 6
            self.expiration_date = self.card_creation_date + relativedelta(months=months)
        
        # Validate trước khi lưu
        self.full_clean()
        
        super().save(*args, **kwargs)


class Author(models.Model):
    """
    Bảng AUTHOR - Tác giả
    """
    author_name = models.CharField(
        max_length=255,
        verbose_name='Tên tác giả'
    )
    bio = models.TextField(
        verbose_name='Tiểu sử',
        blank=True,
        null=True
    )
    
    class Meta:
        db_table = 'author'
        verbose_name = 'Tác giả'
        verbose_name_plural = 'Tác giả'
        ordering = ['author_name']
    
    def __str__(self):
        return self.author_name


class Category(models.Model):
    """
    Bảng CATEGORY - Thể loại sách
    """
    category_name = models.CharField(
        max_length=100,
        verbose_name='Tên thể loại',
        unique=True
    )
    description = models.TextField(
        verbose_name='Mô tả',
        blank=True,
        null=True
    )
    
    class Meta:
        db_table = 'category'
        verbose_name = 'Thể loại'
        verbose_name_plural = 'Thể loại'
        ordering = ['category_name']
    
    def __str__(self):
        return self.category_name


class BookTitle(models.Model):
    """
    Bảng BOOK_TITLE - Tựa sách (đầu sách)
    """
    book_title = models.CharField(
        max_length=500,
        verbose_name='Tên tựa sách'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Thể loại',
        related_name='book_titles'
    )
    authors = models.ManyToManyField(
        Author,
        through='AuthorDetail',
        verbose_name='Tác giả',
        related_name='book_titles'
    )
    description = models.TextField(
        verbose_name='Mô tả',
        blank=True,
        null=True
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'book_title'
        verbose_name = 'Tựa sách'
        verbose_name_plural = 'Tựa sách'
        ordering = ['book_title']
        indexes = [
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.book_title
    
    @property
    def total_books(self):
        """Tổng số sách thuộc tựa sách này"""
        return self.books.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def total_remaining(self):
        """Tổng số sách còn lại chưa mượn"""
        return self.books.aggregate(total=models.Sum('remaining_quantity'))['total'] or 0


class AuthorDetail(models.Model):
    """
    Bảng AUTHOR_DETAIL - Liên kết tác giả và tựa sách (Many-to-Many)
    """
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Tác giả'
    )
    book_title = models.ForeignKey(
        BookTitle,
        on_delete=models.CASCADE,
        verbose_name='Tựa sách'
    )
    
    class Meta:
        db_table = 'author_detail'
        verbose_name = 'Chi tiết tác giả'
        verbose_name_plural = 'Chi tiết tác giả'
        unique_together = [['author', 'book_title']]
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['book_title']),
        ]
    
    def __str__(self):
        return f"{self.author.author_name} - {self.book_title.book_title}"


class Book(models.Model):
    """
    Bảng BOOK - Thông tin sách (một phiên bản cụ thể của tựa sách)
    """
    book_title = models.ForeignKey(
        BookTitle,
        on_delete=models.PROTECT,
        verbose_name='Tựa sách',
        related_name='books'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Số lượng',
        default=1,
        validators=[MinValueValidator(1)]
    )
    unit_price = models.PositiveIntegerField(
        verbose_name='Đơn giá (VNĐ)',
        validators=[MinValueValidator(0)]
    )
    publish_year = models.PositiveIntegerField(
        verbose_name='Năm xuất bản',
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    publisher = models.CharField(
        max_length=255,
        verbose_name='Nhà xuất bản'
    )
    remaining_quantity = models.PositiveIntegerField(
        verbose_name='Số lượng còn lại',
        validators=[MinValueValidator(0)]
    )
    
    # Thông tin bổ sung
    isbn = models.CharField(
        max_length=20,
        verbose_name='ISBN',
        blank=True,
        null=True
    )
    edition = models.CharField(
        max_length=50,
        verbose_name='Phiên bản',
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=50,
        verbose_name='Ngôn ngữ',
        default='Tiếng Việt'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'book'
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
        ordering = ['-publish_year', 'book_title']
        indexes = [
            models.Index(fields=['book_title']),
            models.Index(fields=['publish_year']),
            models.Index(fields=['publisher']),
        ]
    
    def __str__(self):
        return f"{self.book_title.book_title} ({self.publish_year}) - Còn {self.remaining_quantity} quyển"
    
    @property
    def borrowed_quantity(self):
        """Số lượng đang được mượn"""
        return self.quantity - self.remaining_quantity
    
    @property
    def is_available(self):
        """Kiểm tra còn sách để mượn không"""
        return self.remaining_quantity > 0
    
    def clean(self):
        """Validation"""
        from django.core.exceptions import ValidationError
        
        if self.remaining_quantity > self.quantity:
            raise ValidationError({
                'remaining_quantity': 'Số lượng còn lại không thể lớn hơn tổng số lượng'
            })
        
        # Kiểm tra năm xuất bản theo tham số hệ thống
        try:
            params = Parameter.objects.first()
            if params:
                from datetime import date
                current_year = date.today().year
                min_year = current_year - params.book_return_period
                if self.publish_year < min_year:
                    raise ValidationError({
                        'publish_year': f'Chỉ nhận sách xuất bản từ năm {min_year} trở đi'
                    })
        except:
            pass
    
    def save(self, *args, **kwargs):
        # Khởi tạo remaining_quantity = quantity nếu là sách mới
        if not self.pk and not hasattr(self, '_skip_init'):
            if not hasattr(self, 'remaining_quantity') or self.remaining_quantity is None:
                self.remaining_quantity = self.quantity
        
        self.full_clean()
        super().save(*args, **kwargs)


class BookItem(models.Model):
    """
    Bảng BOOK_ITEM - Cuốn sách cụ thể (từng bản copy vật lý)
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        verbose_name='Sách',
        related_name='book_items'
    )
    is_borrowed = models.BooleanField(
        verbose_name='Đang được mượn',
        default=False
    )
    
    # Thông tin bổ sung
    barcode = models.CharField(
        max_length=50,
        verbose_name='Mã vạch',
        unique=True,
        blank=True,
        null=True
    )
    notes = models.TextField(
        verbose_name='Ghi chú',
        blank=True,
        null=True
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'book_item'
        verbose_name = 'Cuốn sách'
        verbose_name_plural = 'Các cuốn sách'
        ordering = ['book', 'id']
        indexes = [
            models.Index(fields=['book']),
            models.Index(fields=['is_borrowed']),
        ]
    
    def __str__(self):
        status = "Đã mượn" if self.is_borrowed else "Sẵn sàng"
        return f"#{self.id} - {self.book.book_title.book_title} ({status})"
    
    @property
    def status_display(self):
        """Hiển thị trạng thái"""
        return "Đang được mượn" if self.is_borrowed else "Sẵn sàng cho mượn"


# ==================== BOOK IMPORT MANAGEMENT ====================

class BookImportReceipt(models.Model):
    """
    Phiếu nhập sách
    Quản lý việc nhập sách vào thư viện
    """
    total_amount = models.IntegerField(
        default=0,
        verbose_name='Tổng tiền nhập sách'
    )
    import_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Ngày nhập sách'
    )
    created_by = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Người lập phiếu'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Ghi chú'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'book_import_receipt'
        verbose_name = 'Phiếu nhập sách'
        verbose_name_plural = 'Phiếu nhập sách'
        ordering = ['-import_date']
        indexes = [
            models.Index(fields=['-import_date']),
        ]
    
    def __str__(self):
        return f"Phiếu nhập #{self.id} - {self.import_date.strftime('%d/%m/%Y')}"
    
    @property
    def total_books_imported(self):
        """Tổng số sách được nhập"""
        return sum(detail.quantity for detail in self.import_details.all())
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Tính lại tổng tiền
        self.total_amount = sum(
            detail.amount for detail in self.import_details.all()
        )
        if kwargs.get('update_fields') is None:
            super().save(update_fields=['total_amount'])


class BookImportDetail(models.Model):
    """
    Chi tiết phiếu nhập sách
    Ghi nhận thông tin từng loại sách được nhập
    """
    receipt = models.ForeignKey(
        BookImportReceipt,
        on_delete=models.CASCADE,
        related_name='import_details',
        verbose_name='Phiếu nhập'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name='import_details',
        verbose_name='Sách'
    )
    quantity = models.IntegerField(
        verbose_name='Số lượng'
    )
    unit_price = models.IntegerField(
        verbose_name='Đơn giá'
    )
    amount = models.IntegerField(
        default=0,
        verbose_name='Thành tiền'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'book_import_detail'
        verbose_name = 'Chi tiết nhập sách'
        verbose_name_plural = 'Chi tiết nhập sách'
        unique_together = [['receipt', 'book']]
        indexes = [
            models.Index(fields=['receipt']),
            models.Index(fields=['book']),
        ]
    
    def __str__(self):
        return f"{self.receipt} - {self.book.book_title.book_title}"
    
    def save(self, *args, **kwargs):
        # Tự động tính thành tiền
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Cập nhật số lượng sách trong kho
        self.book.quantity += self.quantity
        self.book.remaining_quantity += self.quantity
        self.book.save(update_fields=['quantity', 'remaining_quantity'])
        
        # Tạo các BookItem tương ứng
        for i in range(self.quantity):
            existing_items = BookItem.objects.filter(book=self.book).count()
            barcode = f"{self.book.id:04d}-{existing_items + i + 1:03d}"
            BookItem.objects.create(
                book=self.book,
                barcode=barcode,
                is_borrowed=False
            )
        
        # Cập nhật tổng tiền phiếu nhập
        self.receipt.save()


# ==================== BORROW & RETURN MANAGEMENT ====================

class BorrowReturnReceipt(models.Model):
    """
    Phiếu mượn/trả sách
    Quản lý việc mượn và trả sách của độc giả
    """
    reader = models.ForeignKey(
        Reader,
        on_delete=models.PROTECT,
        related_name='borrow_receipts',
        verbose_name='Độc giả'
    )
    book_item = models.ForeignKey(
        BookItem,
        on_delete=models.PROTECT,
        related_name='borrow_receipts',
        verbose_name='Cuốn sách'
    )
    borrow_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Ngày mượn'
    )
    due_date = models.DateTimeField(
        verbose_name='Ngày phải trả'
    )
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ngày thực trả'
    )
    fine_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Tiền phạt trả trễ'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Ghi chú'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'borrow_return_receipt'
        verbose_name = 'Phiếu mượn/trả sách'
        verbose_name_plural = 'Phiếu mượn/trả sách'
        ordering = ['-borrow_date']
        indexes = [
            models.Index(fields=['reader']),
            models.Index(fields=['book_item']),
            models.Index(fields=['-borrow_date']),
            models.Index(fields=['return_date']),
        ]
    
    def __str__(self):
        return f"Phiếu #{self.id} - {self.reader.reader_name} - {self.book_item}"
    
    @property
    def is_returned(self):
        """Kiểm tra đã trả sách chưa"""
        return self.return_date is not None
    
    @property
    def is_overdue(self):
        """Kiểm tra có trễ hạn không"""
        if self.is_returned:
            return self.return_date > self.due_date
        return timezone.now() > self.due_date
    
    @property
    def days_overdue(self):
        """Số ngày trễ hạn"""
        if not self.is_overdue:
            return 0
        
        if self.is_returned:
            delta = self.return_date - self.due_date
        else:
            delta = timezone.now() - self.due_date
        
        return max(0, delta.days)
    
    def calculate_fine(self):
        """Tính tiền phạt dựa trên số ngày trễ"""
        if not self.is_overdue:
            return 0
        
        try:
            param = Parameter.objects.first()
            return self.days_overdue * param.fine_rate
        except:
            return 0
    
    def clean(self):
        """Validate dữ liệu"""
        # Kiểm tra ngày phải trả không nhỏ hơn ngày mượn
        if self.due_date and self.borrow_date and self.due_date < self.borrow_date:
            raise ValidationError({
                'due_date': 'Ngày phải trả không được nhỏ hơn ngày mượn'
            })
        
        # Kiểm tra ngày thực trả không nhỏ hơn ngày mượn
        if self.return_date and self.return_date < self.borrow_date:
            raise ValidationError({
                'return_date': 'Ngày thực trả không được nhỏ hơn ngày mượn'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Nếu chưa có due_date, tính từ borrow_date + max_borrow_days
        if not self.due_date:
            try:
                param = Parameter.objects.first()
                self.due_date = self.borrow_date + timezone.timedelta(days=param.max_borrow_days)
            except:
                self.due_date = self.borrow_date + timezone.timedelta(days=30)
        
        # Tự động tính tiền phạt nếu trả trễ
        if self.return_date and self.is_overdue:
            self.fine_amount = self.calculate_fine()
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Cập nhật trạng thái sách
        if is_new:
            # Mượn sách mới
            self.book_item.is_borrowed = True
            self.book_item.save(update_fields=['is_borrowed'])
            self.book_item.book.remaining_quantity -= 1
            self.book_item.book.save(update_fields=['remaining_quantity'])
        elif self.return_date:
            # Trả sách
            self.book_item.is_borrowed = False
            self.book_item.save(update_fields=['is_borrowed'])
            self.book_item.book.remaining_quantity += 1
            self.book_item.book.save(update_fields=['remaining_quantity'])
            
            # Cập nhật nợ của độc giả
            if self.fine_amount > 0:
                self.reader.total_debt += self.fine_amount
                self.reader.save(update_fields=['total_debt'])


# ==================== PAYMENT MANAGEMENT ====================

class Receipt(models.Model):
    """
    Phiếu thu tiền
    Quản lý việc thu tiền phạt từ độc giả
    """
    reader = models.ForeignKey(
        Reader,
        on_delete=models.PROTECT,
        related_name='payment_receipts',
        verbose_name='Độc giả'
    )
    collected_amount = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Số tiền thu'
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Ngày lập phiếu'
    )
    payment_method = models.CharField(
        max_length=50,
        default='Tiền mặt',
        verbose_name='Phương thức thanh toán'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Ghi chú'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'receipt'
        verbose_name = 'Phiếu thu'
        verbose_name_plural = 'Phiếu thu'
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['reader']),
            models.Index(fields=['-created_date']),
        ]
    
    def __str__(self):
        return f"Phiếu thu #{self.id} - {self.reader.reader_name} - {self.collected_amount:,}đ"
    
    def clean(self):
        """Validate số tiền thu"""
        try:
            param = Parameter.objects.first()
            if param and param.enable_receipt_amount_validation:
                if self.collected_amount > self.reader.total_debt:
                    raise ValidationError({
                        'collected_amount': f'Số tiền thu không được vượt quá tổng nợ ({self.reader.total_debt:,}đ)'
                    })
        except Parameter.DoesNotExist:
            pass
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Trừ nợ của độc giả
        self.reader.total_debt -= self.collected_amount
        self.reader.save(update_fields=['total_debt'])


# ==================== REPORTING ====================

class ReportDetailByCategory(models.Model):
    """
    Báo cáo thống kê mượn sách theo thể loại
    Tổng hợp số lượt mượn theo tháng/năm
    """
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Tháng'
    )
    year = models.IntegerField(
        validators=[MinValueValidator(2000)],
        verbose_name='Năm'
    )
    total_borrow_count = models.IntegerField(
        default=0,
        verbose_name='Tổng số lượt mượn'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'report_detail_by_category'
        verbose_name = 'Báo cáo mượn sách theo thể loại'
        verbose_name_plural = 'Báo cáo mượn sách theo thể loại'
        unique_together = [['month', 'year']]
        ordering = ['-year', '-month']
        indexes = [
            models.Index(fields=['month', 'year']),
        ]
    
    def __str__(self):
        return f"Báo cáo tháng {self.month}/{self.year}"


class BorrowReportDetailByCategory(models.Model):
    """
    Chi tiết báo cáo mượn sách theo thể loại
    Phân tích số lượt mượn và tỉ lệ theo từng tựa sách
    """
    report = models.ForeignKey(
        ReportDetailByCategory,
        on_delete=models.CASCADE,
        related_name='borrow_details',
        verbose_name='Báo cáo'
    )
    book_title = models.ForeignKey(
        BookTitle,
        on_delete=models.PROTECT,
        related_name='borrow_reports',
        verbose_name='Tựa sách'
    )
    borrow_count = models.IntegerField(
        default=0,
        verbose_name='Số lượt mượn'
    )
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name='Tỉ lệ (%)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'borrow_report_detail_by_category'
        verbose_name = 'Chi tiết báo cáo theo thể loại'
        verbose_name_plural = 'Chi tiết báo cáo theo thể loại'
        unique_together = [['report', 'book_title']]
        indexes = [
            models.Index(fields=['report']),
            models.Index(fields=['book_title']),
        ]
    
    def __str__(self):
        return f"{self.report} - {self.book_title.book_title}"
    
    def save(self, *args, **kwargs):
        # Tự động tính tỉ lệ
        if self.report.total_borrow_count > 0:
            self.rate = (self.borrow_count / self.report.total_borrow_count) * 100
        super().save(*args, **kwargs)


class LateReturnReport(models.Model):
    """
    Báo cáo sách trả trễ
    Theo dõi các cuốn sách bị trả trễ hạn
    """
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Ngày lập báo cáo'
    )
    book_item = models.ForeignKey(
        BookItem,
        on_delete=models.PROTECT,
        related_name='late_reports',
        verbose_name='Cuốn sách'
    )
    borrow_date = models.DateTimeField(
        verbose_name='Ngày mượn'
    )
    late_return_days = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Số ngày trễ'
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.PROTECT,
        related_name='late_reports',
        verbose_name='Độc giả',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'late_return_report'
        verbose_name = 'Báo cáo trả trễ'
        verbose_name_plural = 'Báo cáo trả trễ'
        unique_together = [['date', 'book_item']]
        ordering = ['-date', '-late_return_days']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['book_item']),
        ]
    
    def __str__(self):
        return f"Báo cáo {self.date.strftime('%d/%m/%Y')} - {self.book_item} - Trễ {self.late_return_days} ngày"


# ==================== USER & PERMISSION MANAGEMENT ====================

class UserGroup(models.Model):
    """
    Nhóm người dùng (User Group)
    Phân quyền theo nhóm cho thủ thư
    """
    user_group_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Tên nhóm người dùng'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'user_group'
        verbose_name = 'Nhóm người dùng'
        verbose_name_plural = 'Nhóm người dùng'
        ordering = ['user_group_name']
    
    def __str__(self):
        return self.user_group_name


class Function(models.Model):
    """
    Chức năng (Function)
    Các chức năng/màn hình trong hệ thống
    """
    function_name = models.CharField(
        max_length=100,
        verbose_name='Tên chức năng'
    )
    screen_name = models.CharField(
        max_length=100,
        verbose_name='Tên màn hình'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Mô tả'
    )
    url_pattern = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='URL pattern',
        help_text='VD: /readers/, /books/, /borrow/'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'function'
        verbose_name = 'Chức năng'
        verbose_name_plural = 'Chức năng'
        ordering = ['function_name']
    
    def __str__(self):
        return f"{self.function_name} ({self.screen_name})"


class Permission(models.Model):
    """
    Quyền (Permission)
    Gán quyền sử dụng chức năng cho nhóm người dùng
    """
    user_group = models.ForeignKey(
        UserGroup,
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name='Nhóm người dùng'
    )
    function = models.ForeignKey(
        Function,
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name='Chức năng'
    )
    can_view = models.BooleanField(
        default=True,
        verbose_name='Xem'
    )
    can_add = models.BooleanField(
        default=False,
        verbose_name='Thêm'
    )
    can_edit = models.BooleanField(
        default=False,
        verbose_name='Sửa'
    )
    can_delete = models.BooleanField(
        default=False,
        verbose_name='Xóa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'permission'
        verbose_name = 'Quyền'
        verbose_name_plural = 'Quyền'
        unique_together = [['user_group', 'function']]
        indexes = [
            models.Index(fields=['user_group']),
            models.Index(fields=['function']),
        ]
    
    def __str__(self):
        permissions = []
        if self.can_view: permissions.append('Xem')
        if self.can_add: permissions.append('Thêm')
        if self.can_edit: permissions.append('Sửa')
        if self.can_delete: permissions.append('Xóa')
        return f"{self.user_group.user_group_name} - {self.function.function_name} [{', '.join(permissions)}]"


class LibraryUser(models.Model):
    """
    Người dùng hệ thống (Thủ thư)
    Chỉ dành cho nhân viên thư viện, không phải độc giả
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='library_user',
        verbose_name='Tài khoản Django'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='Họ và tên'
    )
    date_of_birth = models.DateField(
        verbose_name='Ngày sinh'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Chức vụ',
        help_text='VD: Thủ thư trưởng, Thủ thư, Nhân viên...'
    )
    user_group = models.ForeignKey(
        UserGroup,
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='Nhóm người dùng'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Số điện thoại'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    address = models.TextField(
        blank=True,
        verbose_name='Địa chỉ'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Đang hoạt động'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    
    class Meta:
        db_table = 'library_user'
        verbose_name = 'Thủ thư'
        verbose_name_plural = 'Thủ thư'
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['user_group']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.position})"
    
    @property
    def username(self):
        """Tên đăng nhập"""
        return self.user.username
    
    @property
    def age(self):
        """Tính tuổi"""
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
    
    def has_permission(self, function_name, permission_type='view'):
        """
        Kiểm tra quyền truy cập chức năng
        permission_type: 'view', 'add', 'edit', 'delete'
        """
        try:
            permission = Permission.objects.get(
                user_group=self.user_group,
                function__function_name=function_name
            )
            
            if permission_type == 'view':
                return permission.can_view
            elif permission_type == 'add':
                return permission.can_add
            elif permission_type == 'edit':
                return permission.can_edit
            elif permission_type == 'delete':
                return permission.can_delete
            
            return False
        except Permission.DoesNotExist:
            return False
    
    def get_allowed_functions(self):
        """Lấy danh sách chức năng được phép sử dụng"""
        return Function.objects.filter(
            permissions__user_group=self.user_group,
            permissions__can_view=True
        ).distinct()

