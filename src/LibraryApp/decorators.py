"""
Decorators for permission checking
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def get_library_user(user):
    """
    Lấy LibraryUser từ Django User
    Returns None nếu không tìm thấy
    """
    try:
        return user.library_user
    except:
        return None


def check_permission(user, function_name, permission_type='view'):
    """
    Kiểm tra quyền của user với chức năng cụ thể
    - Superuser luôn có tất cả quyền
    - Staff kiểm tra theo Permission model
    """
    if not user.is_authenticated:
        return False
    
    # Superuser có tất cả quyền
    if user.is_superuser:
        return True
    
    # Kiểm tra có phải staff không
    if not user.is_staff:
        return False
    
    # Lấy LibraryUser để kiểm tra quyền chi tiết
    library_user = get_library_user(user)
    if library_user:
        return library_user.has_permission(function_name, permission_type)
    
    # Nếu không có LibraryUser, staff mặc định có quyền view
    return permission_type == 'view'


def permission_required(function_name, permission_type='view'):
    """
    Decorator kiểm tra quyền dựa trên Permission model
    
    Sử dụng:
    @permission_required('Quản lý sách', 'edit')
    def book_edit_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
                return redirect('login')
            
            if not check_permission(request.user, function_name, permission_type):
                action_names = {
                    'view': 'xem',
                    'add': 'thêm',
                    'edit': 'sửa',
                    'delete': 'xóa'
                }
                action = action_names.get(permission_type, permission_type)
                messages.error(request, f'Bạn không có quyền {action} "{function_name}".')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


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
            messages.error(request, 'Chỉ Quản lý mới có quyền truy cập chức năng này.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """
    Decorator yêu cầu người dùng là Thủ thư hoặc Quản lý (is_staff hoặc is_superuser)
    
    Tích hợp Permission model:
    - Superuser có tất cả quyền
    - Staff có LibraryUser: kiểm tra quyền theo Permission model
    - Staff không có LibraryUser: fallback cho phép truy cập (để không break existing views)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Bạn cần đăng nhập để truy cập trang này.')
            return redirect('login')
        
        # Superuser có tất cả quyền
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Không phải staff -> không có quyền
        if not request.user.is_staff:
            messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
            return redirect('home')
        
        # Staff: kiểm tra LibraryUser và Permission
        library_user = get_library_user(request.user)
        if library_user:
            # Có LibraryUser - kiểm tra có ít nhất 1 quyền nào đó
            # (Không block nếu user có ít nhất 1 permission)
            from LibraryApp.models import Permission
            has_any_permission = Permission.objects.filter(
                user_group=library_user.user_group,
                can_view=True
            ).exists()
            
            if not has_any_permission:
                messages.error(request, 'Tài khoản của bạn chưa được phân quyền. Liên hệ quản trị viên.')
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

