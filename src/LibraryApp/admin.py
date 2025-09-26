from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, EmailVerification

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
