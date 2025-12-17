"""
Context processors for permission checking in templates
"""
from .decorators import get_library_user, check_permission


def user_permissions(request):
    """
    Thêm thông tin quyền của user vào context cho tất cả templates.
    
    Sử dụng trong template:
    {% if can_view_readers %}...{% endif %}
    {% if can_add_borrow %}...{% endif %}
    """
    context = {
        'is_manager': False,
        'is_staff': False,
        # Quyền cho từng chức năng
        'can_view_readers': False,
        'can_add_readers': False,
        'can_view_books': False,
        'can_add_books': False,
        'can_view_borrow': False,
        'can_add_borrow': False,
        'can_view_return': False,
        'can_add_return': False,
        'can_view_receipt': False,
        'can_add_receipt': False,
        'can_view_reports': False,
        'can_view_settings': False,
        'can_view_users': False,
        'can_view_permissions': False,
    }
    
    if not request.user.is_authenticated:
        return context
    
    # Superuser có tất cả quyền
    if request.user.is_superuser:
        context['is_manager'] = True
        context['is_staff'] = True
        # Set all permissions to True
        for key in context:
            if key.startswith('can_'):
                context[key] = True
        return context
    
    # Staff user
    if request.user.is_staff:
        context['is_staff'] = True
        
        # Kiểm tra quyền từ Permission model
        library_user = get_library_user(request.user)
        if library_user:
            # Độc giả
            context['can_view_readers'] = library_user.has_permission('Quản lý độc giả', 'view') or library_user.has_permission('Lập thẻ độc giả', 'view')
            context['can_add_readers'] = library_user.has_permission('Lập thẻ độc giả', 'add')
            
            # Sách
            context['can_view_books'] = library_user.has_permission('Quản lý sách', 'view')
            context['can_add_books'] = library_user.has_permission('Nhập sách', 'add')
            
            # Mượn sách
            context['can_view_borrow'] = library_user.has_permission('Mượn sách', 'view')
            context['can_add_borrow'] = library_user.has_permission('Mượn sách', 'add')
            
            # Trả sách
            context['can_view_return'] = library_user.has_permission('Trả sách', 'view')
            context['can_add_return'] = library_user.has_permission('Trả sách', 'add')
            
            # Phiếu thu
            context['can_view_receipt'] = library_user.has_permission('Thu tiền phạt', 'view')
            context['can_add_receipt'] = library_user.has_permission('Thu tiền phạt', 'add')
            
            # Báo cáo
            context['can_view_reports'] = library_user.has_permission('Báo cáo', 'view')
            
            # Cài đặt hệ thống (chỉ manager)
            context['can_view_settings'] = library_user.has_permission('Cài đặt hệ thống', 'view')
            context['can_view_users'] = library_user.has_permission('Quản lý người dùng', 'view')
            context['can_view_permissions'] = library_user.has_permission('Quản lý quyền', 'view')
        else:
            # Staff không có LibraryUser - fallback cho phép view tất cả
            for key in context:
                if key.startswith('can_view'):
                    context[key] = True
                if key.startswith('can_add'):
                    context[key] = True
    
    return context


def site_config(request):
    """
    Thêm thông tin cấu hình site vào context.
    """
    import os
    
    # Kiểm tra xem có chạy trong Docker không (check environment variable)
    is_docker = os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER', False)
    
    if is_docker:
        base_url = os.getenv('PUBLIC_URL', 'http://library.smartxdr.app')
    else:
        # Local development
        base_url = os.getenv('LOCAL_URL', 'http://127.0.0.1:8000')
    
    return {
        'base_url': base_url,
        'is_docker': is_docker,
    }
