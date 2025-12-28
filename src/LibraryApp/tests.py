from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .models import LibraryUser, UserGroup

@override_settings(RATELIMIT_ENABLE=False)
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        
        # Create User Group
        self.group = UserGroup.objects.create(user_group_name='Test Group')
        
        # Create User and LibraryUser
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com', is_staff=True)
        self.lib_user = LibraryUser.objects.create(
            user=self.user,
            full_name='Test User',
            date_of_birth='2000-01-01',
            user_group=self.group
        )
    
    def test_inactive_user_login(self):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Check message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Tài khoản chưa được kích hoạt', str(messages[0]))
    
    def test_user_not_found(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'anypassword'
        })
        form_errors = response.context['form'].non_field_errors()
        self.assertEqual(len(form_errors), 1, "Should have exactly 1 error for user not found")
        self.assertEqual(str(form_errors[0]), 'Tên đăng nhập hoặc mật khẩu không đúng.')

    def test_wrong_password_counting(self):
        # 1st fail
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.lib_user.refresh_from_db()
        self.assertEqual(self.lib_user.failed_login_attempts, 1)
        
        # Check form errors instead of messages
        form_errors = response.context['form'].non_field_errors()
        self.assertTrue(len(form_errors) > 0)
        error_msg = str(form_errors[0])
        # Verify EXACT message content (no generic prefix)
        self.assertEqual(error_msg, 'Sai mật khẩu. Bạn còn 4 lần thử.')
        
    def test_lockout(self):
        # Fail 5 times
        for i in range(5):
            self.client.post(self.login_url, {
                'username': 'testuser',
                'password': 'wrongpassword'
            })
            
        self.lib_user.refresh_from_db()
        self.assertEqual(self.lib_user.failed_login_attempts, 5)
        
        # 6th attempt (even with correct password)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        
        form_errors = response.context['form'].non_field_errors()
        self.assertTrue(len(form_errors) > 0)
        self.assertIn('Tài khoản đã bị khoá', str(form_errors[0]))
        
        # Ensure still locked and not logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_successful_login_resets_counter(self):
        # Fail once
        self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.lib_user.refresh_from_db()
        self.assertEqual(self.lib_user.failed_login_attempts, 1)
        
        # Success
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        }, follow=True)
        
        self.lib_user.refresh_from_db()
        self.assertEqual(self.lib_user.failed_login_attempts, 0)
        self.assertTrue(response.context['user'].is_authenticated)
