from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    UserProfile, EmailVerification,
    Parameter, ReaderType, Reader,
    Author, Category, BookTitle, AuthorDetail, Book, BookItem,
    BookImportReceipt, BookImportDetail,
    BorrowReturnReceipt, Receipt,
    ReportDetailByCategory, BorrowReportDetailByCategory, LateReturnReport
)

# ==================== USER AUTHENTICATION ADMIN ====================

# Inline cho UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('phone_number', 'address', 'date_of_birth', 'is_verified', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

# Extend UserAdmin để bao gồm UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_verified')
    
    def get_is_verified(self, obj):
        try:
            return obj.userprofile.is_verified
        except UserProfile.DoesNotExist:
            return False
    get_is_verified.short_description = 'Verified'
    get_is_verified.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'is_used', 'created_at', 'is_expired_display')
    list_filter = ('is_used', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('user__email', 'user__username')
    
    def is_expired_display(self, obj):
        return obj.is_expired()
    is_expired_display.short_description = 'Expired'
    is_expired_display.boolean = True


# ==================== LIBRARY MANAGEMENT ADMIN ====================

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Quy định về độ tuổi', {
            'fields': ('max_age', 'min_age')
        }),
        ('Quy định về thẻ độc giả', {
            'fields': ('card_validity_period',)
        }),
        ('Quy định về sách', {
            'fields': ('book_return_period', 'max_borrowed_books', 'max_borrow_days')
        }),
        ('Quy định về tiền phạt', {
            'fields': ('fine_rate',)
        }),
        ('Quy định khác', {
            'fields': ('enable_receipt_amount_validation',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Chỉ cho phép 1 bản ghi duy nhất
        return not Parameter.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Không cho xóa tham số hệ thống
        return False


@admin.register(ReaderType)
class ReaderTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'reader_type_name', 'description', 'reader_count')
    search_fields = ('reader_type_name',)
    ordering = ('reader_type_name',)
    
    def reader_count(self, obj):
        return obj.readers.count()
    reader_count.short_description = 'Số độc giả'


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'reader_name', 'email', 'reader_type', 'age_display',
        'card_status', 'total_debt', 'is_active', 'card_creation_date'
    )
    list_filter = ('reader_type', 'is_active', 'card_creation_date')
    search_fields = ('reader_name', 'email', 'phone_number')
    readonly_fields = ('age_display', 'is_card_expired', 'days_until_expiration', 'created_at', 'updated_at')
    date_hierarchy = 'card_creation_date'
    
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('reader_name', 'date_of_birth', 'age_display', 'email', 'phone_number', 'address')
        }),
        ('Phân loại', {
            'fields': ('reader_type',)
        }),
        ('Thông tin thẻ', {
            'fields': ('card_creation_date', 'expiration_date', 'is_card_expired', 'days_until_expiration')
        }),
        ('Thông tin tài chính', {
            'fields': ('total_debt',)
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def age_display(self, obj):
        return f"{obj.age} tuổi"
    age_display.short_description = 'Tuổi'
    
    def card_status(self, obj):
        if obj.is_card_expired:
            return '❌ Hết hạn'
        elif obj.days_until_expiration <= 30:
            return f'⚠️ Còn {obj.days_until_expiration} ngày'
        else:
            return f'✓ Còn {obj.days_until_expiration} ngày'
    card_status.short_description = 'Trạng thái thẻ'
    
    actions = ['activate_readers', 'deactivate_readers']
    
    def activate_readers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Đã kích hoạt {updated} độc giả.')
    activate_readers.short_description = 'Kích hoạt độc giả đã chọn'
    
    def deactivate_readers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Đã vô hiệu hóa {updated} độc giả.')
    deactivate_readers.short_description = 'Vô hiệu hóa độc giả đã chọn'


# ==================== BOOK MANAGEMENT ADMIN ====================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'book_count')
    search_fields = ('author_name',)
    ordering = ('author_name',)
    
    def book_count(self, obj):
        return obj.book_titles.count()
    book_count.short_description = 'Số tựa sách'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description', 'book_title_count')
    search_fields = ('category_name',)
    ordering = ('category_name',)
    
    def book_title_count(self, obj):
        return obj.book_titles.count()
    book_title_count.short_description = 'Số tựa sách'


class AuthorDetailInline(admin.TabularInline):
    model = AuthorDetail
    extra = 1
    verbose_name = 'Tác giả'
    verbose_name_plural = 'Các tác giả'


@admin.register(BookTitle)
class BookTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'category', 'author_list', 'total_books_display', 'total_remaining_display')
    list_filter = ('category',)
    search_fields = ('book_title', 'authors__author_name')
    inlines = [AuthorDetailInline]
    readonly_fields = ('total_books_display', 'total_remaining_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('book_title', 'category', 'description')
        }),
        ('Thống kê', {
            'fields': ('total_books_display', 'total_remaining_display')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_list(self, obj):
        return ", ".join([author.author_name for author in obj.authors.all()[:3]])
    author_list.short_description = 'Tác giả'
    
    def total_books_display(self, obj):
        return obj.total_books
    total_books_display.short_description = 'Tổng số sách'
    
    def total_remaining_display(self, obj):
        return obj.total_remaining
    total_remaining_display.short_description = 'Còn lại'


class BookItemInline(admin.TabularInline):
    model = BookItem
    extra = 0
    fields = ('id', 'barcode', 'is_borrowed', 'notes')
    readonly_fields = ('id',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_title', 'publisher', 'publish_year', 
        'quantity', 'remaining_quantity', 'borrowed_quantity_display', 
        'availability_status'
    )
    list_filter = ('publish_year', 'publisher', 'book_title__category')
    search_fields = ('book_title__book_title', 'publisher', 'isbn')
    readonly_fields = ('borrowed_quantity_display', 'created_at', 'updated_at')
    inlines = [BookItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông tin tựa sách', {
            'fields': ('book_title',)
        }),
        ('Thông tin xuất bản', {
            'fields': ('publisher', 'publish_year', 'isbn', 'edition', 'language')
        }),
        ('Thông tin số lượng', {
            'fields': ('quantity', 'remaining_quantity', 'borrowed_quantity_display', 'unit_price')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_title(self, obj):
        return obj.book_title.book_title
    get_title.short_description = 'Tựa sách'
    get_title.admin_order_field = 'book_title__book_title'
    
    def borrowed_quantity_display(self, obj):
        return obj.borrowed_quantity
    borrowed_quantity_display.short_description = 'Đang mượn'
    
    def availability_status(self, obj):
        if obj.remaining_quantity == 0:
            return '❌ Hết sách'
        elif obj.remaining_quantity < obj.quantity * 0.2:
            return f'⚠️ Còn {obj.remaining_quantity}'
        else:
            return f'✓ Còn {obj.remaining_quantity}'
    availability_status.short_description = 'Tình trạng'


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_book_title', 'get_publisher', 'barcode', 'status_display_admin', 'created_at')
    list_filter = ('is_borrowed', 'book__publish_year', 'book__book_title__category')
    search_fields = ('book__book_title__book_title', 'barcode', 'notes')
    readonly_fields = ('status_display', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông tin sách', {
            'fields': ('book', 'barcode')
        }),
        ('Trạng thái', {
            'fields': ('is_borrowed', 'status_display')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_book_title(self, obj):
        return obj.book.book_title.book_title
    get_book_title.short_description = 'Tựa sách'
    get_book_title.admin_order_field = 'book__book_title__book_title'
    
    def get_publisher(self, obj):
        return f"{obj.book.publisher} ({obj.book.publish_year})"
    get_publisher.short_description = 'Xuất bản'
    
    def status_display_admin(self, obj):
        return '📕 Đang mượn' if obj.is_borrowed else '📗 Sẵn sàng'
    status_display_admin.short_description = 'Trạng thái'
    
    actions = ['mark_as_borrowed', 'mark_as_available']
    
    def mark_as_borrowed(self, request, queryset):
        updated = queryset.filter(is_borrowed=False).update(is_borrowed=True)
        self.message_user(request, f'Đã đánh dấu {updated} cuốn sách là đang mượn.')
    mark_as_borrowed.short_description = 'Đánh dấu đang mượn'
    
    def mark_as_available(self, request, queryset):
        updated = queryset.filter(is_borrowed=True).update(is_borrowed=False)
        self.message_user(request, f'Đã đánh dấu {updated} cuốn sách là sẵn sàng.')
    mark_as_available.short_description = 'Đánh dấu sẵn sàng'


# ==================== BOOK IMPORT ADMIN ====================

class BookImportDetailInline(admin.TabularInline):
    model = BookImportDetail
    extra = 1
    fields = ('book', 'quantity', 'unit_price', 'amount')
    readonly_fields = ('amount',)


@admin.register(BookImportReceipt)
class BookImportReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'import_date', 'total_amount_display', 'total_books_display', 'created_by')
    list_filter = ('import_date',)
    search_fields = ('created_by', 'notes')
    readonly_fields = ('total_amount', 'total_books_display', 'created_at', 'updated_at')
    date_hierarchy = 'import_date'
    inlines = [BookImportDetailInline]
    
    fieldsets = (
        ('Thông tin phiếu nhập', {
            'fields': ('import_date', 'created_by')
        }),
        ('Thống kê', {
            'fields': ('total_amount', 'total_books_display')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_amount_display(self, obj):
        return f"{obj.total_amount:,}đ"
    total_amount_display.short_description = 'Tổng tiền'
    total_amount_display.admin_order_field = 'total_amount'
    
    def total_books_display(self, obj):
        return obj.total_books_imported
    total_books_display.short_description = 'Tổng số sách'


@admin.register(BookImportDetail)
class BookImportDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt', 'get_book_title', 'quantity', 'unit_price_display', 'amount_display')
    list_filter = ('receipt__import_date', 'book__book_title__category')
    search_fields = ('receipt__id', 'book__book_title__book_title')
    readonly_fields = ('amount', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin nhập', {
            'fields': ('receipt', 'book', 'quantity', 'unit_price', 'amount')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_book_title(self, obj):
        return f"{obj.book.book_title.book_title} ({obj.book.publish_year})"
    get_book_title.short_description = 'Sách'
    
    def unit_price_display(self, obj):
        return f"{obj.unit_price:,}đ"
    unit_price_display.short_description = 'Đơn giá'
    unit_price_display.admin_order_field = 'unit_price'
    
    def amount_display(self, obj):
        return f"{obj.amount:,}đ"
    amount_display.short_description = 'Thành tiền'
    amount_display.admin_order_field = 'amount'


# ==================== BORROW & RETURN ADMIN ====================

@admin.register(BorrowReturnReceipt)
class BorrowReturnReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_reader', 'get_book', 'borrow_date', 'due_date',
        'return_date', 'status_display', 'fine_amount_display'
    )
    list_filter = ('borrow_date', 'return_date', 'reader__reader_type')
    search_fields = ('reader__reader_name', 'book_item__book__book_title__book_title', 'book_item__barcode')
    readonly_fields = ('is_returned', 'is_overdue', 'days_overdue', 'created_at', 'updated_at')
    date_hierarchy = 'borrow_date'
    
    fieldsets = (
        ('Thông tin mượn sách', {
            'fields': ('reader', 'book_item', 'borrow_date', 'due_date')
        }),
        ('Thông tin trả sách', {
            'fields': ('return_date', 'fine_amount')
        }),
        ('Trạng thái', {
            'fields': ('is_returned', 'is_overdue', 'days_overdue')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_reader(self, obj):
        return obj.reader.reader_name
    get_reader.short_description = 'Độc giả'
    get_reader.admin_order_field = 'reader__reader_name'
    
    def get_book(self, obj):
        return f"{obj.book_item.book.book_title.book_title} ({obj.book_item.barcode})"
    get_book.short_description = 'Sách'
    
    def status_display(self, obj):
        if obj.is_returned:
            return '✓ Đã trả'
        elif obj.is_overdue:
            return f'⚠️ Quá hạn {obj.days_overdue} ngày'
        else:
            return '📖 Đang mượn'
    status_display.short_description = 'Trạng thái'
    
    def fine_amount_display(self, obj):
        if obj.fine_amount > 0:
            return f"{obj.fine_amount:,}đ"
        return '-'
    fine_amount_display.short_description = 'Tiền phạt'
    fine_amount_display.admin_order_field = 'fine_amount'


# ==================== PAYMENT ADMIN ====================

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'reader', 'collected_amount_display', 'created_date', 'payment_method')
    list_filter = ('created_date', 'payment_method')
    search_fields = ('reader__reader_name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Thông tin phiếu thu', {
            'fields': ('reader', 'collected_amount', 'payment_method', 'created_date')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def collected_amount_display(self, obj):
        return f"{obj.collected_amount:,}đ"
    collected_amount_display.short_description = 'Số tiền thu'
    collected_amount_display.admin_order_field = 'collected_amount'


# ==================== REPORTING ADMIN ====================

class BorrowReportDetailInline(admin.TabularInline):
    model = BorrowReportDetailByCategory
    extra = 0
    fields = ('book_title', 'borrow_count', 'rate')
    readonly_fields = ('rate',)


@admin.register(ReportDetailByCategory)
class ReportDetailByCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'month', 'year', 'total_borrow_count', 'detail_count')
    list_filter = ('year', 'month')
    search_fields = ('month', 'year')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [BorrowReportDetailInline]
    
    fieldsets = (
        ('Thời gian báo cáo', {
            'fields': ('month', 'year')
        }),
        ('Thống kê', {
            'fields': ('total_borrow_count',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def detail_count(self, obj):
        return obj.borrow_details.count()
    detail_count.short_description = 'Số thể loại'


@admin.register(BorrowReportDetailByCategory)
class BorrowReportDetailByCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'book_title', 'borrow_count', 'rate_display')
    list_filter = ('report__year', 'report__month', 'book_title__category')
    search_fields = ('book_title__book_title',)
    readonly_fields = ('rate', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin báo cáo', {
            'fields': ('report', 'book_title')
        }),
        ('Thống kê', {
            'fields': ('borrow_count', 'rate')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rate_display(self, obj):
        return f"{obj.rate:.2f}%"
    rate_display.short_description = 'Tỉ lệ'
    rate_display.admin_order_field = 'rate'


@admin.register(LateReturnReport)
class LateReturnReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'get_reader', 'get_book', 'borrow_date', 'late_return_days_display')
    list_filter = ('date', 'reader__reader_type')
    search_fields = ('book_item__book__book_title__book_title', 'reader__reader_name', 'book_item__barcode')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Thông tin báo cáo', {
            'fields': ('date', 'reader', 'book_item')
        }),
        ('Chi tiết', {
            'fields': ('borrow_date', 'late_return_days')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_reader(self, obj):
        return obj.reader.reader_name if obj.reader else 'N/A'
    get_reader.short_description = 'Độc giả'
    
    def get_book(self, obj):
        return f"{obj.book_item.book.book_title.book_title} ({obj.book_item.barcode})"
    get_book.short_description = 'Sách'
    
    def late_return_days_display(self, obj):
        if obj.late_return_days > 7:
            return f'🔴 {obj.late_return_days} ngày'
        elif obj.late_return_days > 3:
            return f'⚠️ {obj.late_return_days} ngày'
        else:
            return f'{obj.late_return_days} ngày'
    late_return_days_display.short_description = 'Số ngày trễ'
    late_return_days_display.admin_order_field = 'late_return_days'

