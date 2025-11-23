"""
Decorators for permission checking
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def manager_required(view_func):
    """
    Decorator yêu cầu người dùng là Quản lý (is_superuser)
    
    Quyền hạn chỉ dành cho Quản lý:
    - Phân quyền cho người dùng
    - Quản lý người dùng
    - Thay đổi quy định
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
            return redirect('login')
        
        if not request.user.is_superuser:
            messages.error(request, '⛔ Chỉ Quản lý mới có quyền truy cập chức năng này.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """
    Decorator yêu cầu người dùng là Thủ thư hoặc Quản lý (is_staff hoặc is_superuser)
    
    Quyền hạn dành cho cả Quản lý và Thủ thư:
    - Quản lý phiếu mượn trả sách
    - Lập báo cáo
    - Lập phiếu thu tiền phạt
    - Quản lý độc giả
    - Tra cứu sách
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
            return redirect('login')
        
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, '⛔ Bạn không có quyền truy cập chức năng này.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def get_user_role_display(user):
    """
    Trả về vai trò của người dùng dưới dạng text
    """
    if user.is_superuser:
        return "Quản lý"
    elif user.is_staff:
        return "Thủ thư"
    else:
        return "Người dùng"


def has_manager_permission(user):
    """
    Kiểm tra xem user có quyền Quản lý không
    """
    return user.is_authenticated and user.is_superuser


def has_staff_permission(user):
    """
    Kiểm tra xem user có quyền Thủ thư hoặc Quản lý không
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)
