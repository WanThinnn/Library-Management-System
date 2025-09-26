from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponse
from .models import UserProfile, EmailVerification
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordResetForm, CustomSetPasswordForm

def home_view(request):
    return render(request, 'LibraryApp/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            user.save()
            
            # Tạo token xác thực
            token = get_random_string(50)
            verification = EmailVerification.objects.create(user=user, token=token)
            
            # Gửi email xác thực
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token})
            )
            
            subject = 'Xác thực tài khoản - Thư viện'
            message = f'''
            Chào {user.first_name},
            
            Cảm ơn bạn đã đăng ký tài khoản. Vui lòng click vào link dưới đây để xác thực tài khoản:
            
            {verification_url}
            
            Link này sẽ hết hạn sau 1 giờ.
            
            Trân trọng,
            Hệ thống quản lý thư viện
            '''
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, 'Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Có lỗi xảy ra khi gửi email xác thực. Vui lòng thử lại.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Chào mừng {user.first_name}!')
            return redirect('home')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('login')

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token, is_used=False)
        
        if verification.is_expired():
            messages.error(request, 'Link xác thực đã hết hạn.')
            return redirect('login')
        
        user = verification.user
        # Cập nhật profile thay vì user
        try:
            profile = UserProfile.objects.get(user=user)
            profile.is_verified = True
            profile.save()
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user, is_verified=True)
        
        verification.is_used = True
        verification.save()
        
        messages.success(request, 'Tài khoản đã được xác thực thành công! Bạn có thể đăng nhập ngay bây giờ.')
        return redirect('login')
        
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Link xác thực không hợp lệ.')
        return redirect('login')

def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Kiểm tra profile
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.is_verified:
                    messages.error(request, 'Tài khoản đã được xác thực.')
                    return redirect('login')
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user, is_verified=False)
            
            # Xóa token cũ nếu có
            EmailVerification.objects.filter(user=user).delete()
            
            # Tạo token mới
            token = get_random_string(50)
            verification = EmailVerification.objects.create(user=user, token=token)
            
            # Gửi email
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token})
            )
            
            subject = 'Xác thực tài khoản - Thư viện'
            message = f'''
            Chào {user.first_name},
            
            Vui lòng click vào link dưới đây để xác thực tài khoản:
            
            {verification_url}
            
            Link này sẽ hết hạn sau 1 giờ.
            
            Trân trọng,
            Hệ thống quản lý thư viện
            '''
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, 'Email xác thực đã được gửi lại!')
            
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy tài khoản chưa xác thực với email này.')
    
    return render(request, 'accounts/resend_verification.html')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')