from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được đăng ký.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Tạo profile
            profile = UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                is_verified=False
            )
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                # Kiểm tra xem có profile và đã verified chưa
                try:
                    profile = UserProfile.objects.get(user=user)
                    if not profile.is_verified:
                        raise forms.ValidationError("Tài khoản chưa được xác thực. Vui lòng kiểm tra email.")
                except UserProfile.DoesNotExist:
                    # Tạo profile nếu chưa có
                    UserProfile.objects.create(user=user, is_verified=False)
                    raise forms.ValidationError("Tài khoản chưa được xác thực. Vui lòng kiểm tra email.")
                
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError("Email hoặc mật khẩu không đúng.")
                else:
                    self.confirm_login_allowed(self.user_cache)
            except User.DoesNotExist:
                raise forms.ValidationError("Email hoặc mật khẩu không đúng.")

        return self.cleaned_data

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Không tìm thấy tài khoản với email này.")
        return email

class CustomSetPasswordForm(SetPasswordForm):
    pass