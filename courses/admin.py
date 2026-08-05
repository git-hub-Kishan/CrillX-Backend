from django.contrib import admin
from .models import CreatorCourse

@admin.register(CreatorCourse)
class CreatorCourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'user', 'course_language', 'is_published', 'is_locked', 'created_at')
    list_filter = ('is_published', 'is_locked', 'course_language')
    search_fields = ('course_name', 'user__email', 'user__username')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-created_at',)
