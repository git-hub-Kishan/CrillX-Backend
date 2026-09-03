from django.contrib import admin
from .models import CreatorCourse, CourseModule


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    readonly_fields = ('uuid', 'created_at', 'updated_at')


@admin.register(CreatorCourse)
class CreatorCourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'user', 'course_language', 'is_published', 'is_locked', 'created_at')
    list_filter = ('is_published', 'is_locked', 'course_language')
    search_fields = ('course_name', 'user__email', 'user__username')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [CourseModuleInline]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('module_title', 'course', 'order', 'duration_in_seconds', 'is_preview', 'created_at')
    list_filter = ('is_preview', 'course')
    search_fields = ('module_title', 'course__course_name', 'what_you_will_learn')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('course', 'order', '-created_at')

