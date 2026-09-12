from django.contrib import admin
from admin.models import HeaderGIFBanner


@admin.register(HeaderGIFBanner)
class HeaderGIFBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'occasion', 'target_audience', 'is_active', 'start_date_time', 'end_date_time', 'created_at')
    list_filter = ('is_active', 'target_audience', 'occasion')
    search_fields = ('title', 'occasion')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
