"""
Management command to setup default permission data
Creates default UserGroups, Functions, and Permissions
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from LibraryApp.models import UserGroup, Function, Permission, LibraryUser


class Command(BaseCommand):
    help = 'Setup default permission data (UserGroups, Functions, Permissions)'

    def handle(self, *args, **options):
        self.stdout.write('Setting up permission system...\n')
        
        # 1. Create default UserGroups
        self.stdout.write('Creating UserGroups...')
        groups_data = [
            {'user_group_name': 'Quản lý', 'description': 'Quản lý hệ thống - có tất cả quyền'},
            {'user_group_name': 'Thủ thư', 'description': 'Nhân viên thư viện - quyền hạn chế'},
        ]
        
        groups = {}
        for data in groups_data:
            group, created = UserGroup.objects.get_or_create(
                user_group_name=data['user_group_name'],
                defaults={'description': data['description']}
            )
            groups[data['user_group_name']] = group
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"  - {data['user_group_name']}: {status}")
        
        # 2. Create default Functions
        self.stdout.write('\nCreating Functions...')
        functions_data = [
            {'function_name': 'Quản lý độc giả', 'screen_name': 'Danh sách độc giả', 'url_pattern': '/readers/'},
            {'function_name': 'Lập thẻ độc giả', 'screen_name': 'Tạo thẻ độc giả', 'url_pattern': '/reader/create/'},
            {'function_name': 'Quản lý sách', 'screen_name': 'Tra cứu sách', 'url_pattern': '/books/search/'},
            {'function_name': 'Nhập sách', 'screen_name': 'Tiếp nhận sách mới', 'url_pattern': '/book/import/'},
            {'function_name': 'Mượn sách', 'screen_name': 'Cho mượn sách', 'url_pattern': '/book/borrow/'},
            {'function_name': 'Trả sách', 'screen_name': 'Nhận trả sách', 'url_pattern': '/book/return/'},
            {'function_name': 'Thu tiền phạt', 'screen_name': 'Lập phiếu thu', 'url_pattern': '/receipt/'},
            {'function_name': 'Báo cáo', 'screen_name': 'Lập báo cáo', 'url_pattern': '/report/'},
            {'function_name': 'Cài đặt hệ thống', 'screen_name': 'Thay đổi quy định', 'url_pattern': '/parameters/'},
            {'function_name': 'Quản lý người dùng', 'screen_name': 'Danh sách người dùng', 'url_pattern': '/users/'},
            {'function_name': 'Quản lý quyền', 'screen_name': 'Phân quyền', 'url_pattern': '/permissions/'},
        ]
        
        functions = {}
        for data in functions_data:
            func, created = Function.objects.get_or_create(
                function_name=data['function_name'],
                defaults={
                    'screen_name': data['screen_name'],
                    'url_pattern': data['url_pattern']
                }
            )
            functions[data['function_name']] = func
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"  - {data['function_name']}: {status}")
        
        # 3. Create default Permissions for Thủ thư (Quản lý has all via is_superuser)
        self.stdout.write('\nCreating Permissions for Thủ thư...')
        thu_thu = groups.get('Thủ thư')
        
        if thu_thu:
            # Thủ thư permissions - can view/add/edit most things
            thu_thu_permissions = {
                'Quản lý độc giả': {'can_view': True, 'can_add': True, 'can_edit': True, 'can_delete': False},
                'Lập thẻ độc giả': {'can_view': True, 'can_add': True, 'can_edit': True, 'can_delete': False},
                'Quản lý sách': {'can_view': True, 'can_add': False, 'can_edit': False, 'can_delete': False},
                'Nhập sách': {'can_view': True, 'can_add': True, 'can_edit': False, 'can_delete': False},
                'Mượn sách': {'can_view': True, 'can_add': True, 'can_edit': False, 'can_delete': False},
                'Trả sách': {'can_view': True, 'can_add': True, 'can_edit': False, 'can_delete': False},
                'Thu tiền phạt': {'can_view': True, 'can_add': True, 'can_edit': False, 'can_delete': False},
                'Báo cáo': {'can_view': True, 'can_add': False, 'can_edit': False, 'can_delete': False},
                'Cài đặt hệ thống': {'can_view': False, 'can_add': False, 'can_edit': False, 'can_delete': False},
                'Quản lý người dùng': {'can_view': False, 'can_add': False, 'can_edit': False, 'can_delete': False},
                'Quản lý quyền': {'can_view': False, 'can_add': False, 'can_edit': False, 'can_delete': False},
            }
            
            for func_name, perms in thu_thu_permissions.items():
                func = functions.get(func_name)
                if func:
                    perm, created = Permission.objects.update_or_create(
                        user_group=thu_thu,
                        function=func,
                        defaults=perms
                    )
                    status = 'Created' if created else 'Updated'
                    self.stdout.write(f"  - {func_name}: {status}")
        
        # 4. Link existing staff users to LibraryUser if not already linked
        self.stdout.write('\nChecking staff users...')
        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        
        for user in staff_users:
            try:
                library_user = user.library_user
                self.stdout.write(f"  - {user.username}: Already linked to {library_user.user_group.user_group_name}")
            except:
                self.stdout.write(f"  - {user.username}: NOT linked to LibraryUser (needs manual setup)")
        
        self.stdout.write(self.style.SUCCESS('\n✓ Permission system setup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Go to /permissions/groups/ to manage group permissions')
        self.stdout.write('2. Go to /permissions/functions/ to add/edit functions')
        self.stdout.write('3. For staff users without LibraryUser, create one manually or via admin')
