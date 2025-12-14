from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Quản lý người dùng (CHỈ QUẢN LÝ)
    path('users/', views.user_list_view, name='user_list'),
    path('user/create/', views.user_create_view, name='user_create'),
    path('user/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('user/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('profile/', views.user_profile_view, name='user_profile'),
    
    # YC1: Lập thẻ độc giả
    path('reader/create/', views.reader_create_view, name='reader_create'),
    path('reader/<int:reader_id>/', views.reader_detail_view, name='reader_detail'),
    path('readers/', views.reader_list_view, name='reader_list'),
    
    # YC2: Tiếp nhận sách mới
    path('book/import/', views.book_import_view, name='book_import'),
    path('book/import/<int:import_id>/', views.book_import_detail_view, name='book_import_detail'),
    path('books/import/', views.book_import_list_view, name='book_import_list'),
    
    # YC3: Tra cứu sách
    path('books/search/', views.book_search_view, name='book_search'),
    
    # YC4: Cho mượn sách
    path('book/borrow/', views.borrow_book_view, name='borrow_book'),
    path('book/borrow/<int:receipt_id>/', views.borrow_book_detail_view, name='borrow_book_detail'),
    path('books/borrow/', views.borrow_book_list_view, name='borrow_book_list'),
    
    # YC5: Nhận trả sách
    path('book/return/', views.return_book_view, name='return_book'),
    path('book/return/<int:receipt_id>/', views.return_book_detail_view, name='return_book_detail'),
    path('books/return/', views.return_book_list_view, name='return_book_list'),
    
    # API endpoints for borrow book
    path('api/readers/', views.api_readers_list, name='api_readers'),
    path('api/books/', views.api_books_list, name='api_books'),
    path('api/borrowing-readers/', views.api_borrowing_readers, name='api_borrowing_readers'),
    
    # API endpoints for return book
    path('api/unreturned-receipts/', views.api_unreturned_receipts, name='api_unreturned_receipts'),
    path('api/reader/<int:reader_id>/borrowed-books/', views.api_reader_borrowed_books, name='api_reader_borrowed_books'),
    
    # YC6: Lập phiếu thu tiền phạt
    path('receipt/', views.receipt_form_view, name='receipt_form'),
    path('receipt/<int:receipt_id>/', views.receipt_detail_view, name='receipt_detail'),
    path('receipts/', views.receipt_list_view, name='receipt_list'),
    
    # API endpoints for receipt
    path('api/reader/<int:reader_id>/debt/', views.api_reader_debt, name='api_reader_debt'),
    
    # YC7: Lập báo cáo
    path('report/borrow-by-category/', views.report_borrow_by_category_view, name='report_borrow_by_category'),
    path('report/borrow-by-category/excel/', views.report_borrow_by_category_excel, name='report_borrow_by_category_excel'),
    path('report/overdue-books/', views.report_overdue_books_view, name='report_overdue_books'),
    path('report/overdue-books/excel/', views.report_overdue_books_excel, name='report_overdue_books_excel'),
    path('report/borrow-situation/', views.report_borrow_situation_view, name='report_borrow_situation'),
    path('report/borrow-situation/excel/', views.report_borrow_situation_excel, name='report_borrow_situation_excel'),
    
    # YC8: Thay đổi quy định
    path('parameters/', views.parameter_update_view, name='parameter_update'),
    
    # Book Detail & Edit
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/<int:book_id>/edit/', views.book_edit_view, name='book_edit'),
    
    # Reader Type Management
    path('reader-types/', views.reader_type_list_view, name='reader_type_list'),
    path('reader-type/create/', views.reader_type_create_view, name='reader_type_create'),
    path('reader-type/<int:reader_type_id>/edit/', views.reader_type_edit_view, name='reader_type_edit'),
    path('reader-type/<int:reader_type_id>/delete/', views.reader_type_delete_view, name='reader_type_delete'),
]
