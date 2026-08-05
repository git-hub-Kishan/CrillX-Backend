from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CreatorProfile, LearnerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'full_name', 'user_type', 'signup_type', 'is_verified', 'is_active', 'is_staff', 'last_login')
    list_filter = ('user_type', 'signup_type', 'is_verified', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'uuid', 'phone_number')
    readonly_fields = ('uuid', 'created_at', 'updated_at', 'last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'uuid')}),
        ('User Type & Verification', {'fields': ('user_type', 'signup_type', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teaching_category', 'profession', 'experience', 'state', 'city', 'created_at')
    list_filter = ('teaching_category', 'profession', 'experience', 'state')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'yt_username', 'insta_username', 'city')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'state', 'city', 'created_at')
    list_filter = ('profession', 'state')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city')
    readonly_fields = ('created_at', 'updated_at')
