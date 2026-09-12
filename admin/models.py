import uuid
from django.db import models
from admin.helpers.banner_helpers import TargetAudience


class HeaderGIFBanner(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=100)
    file_key = models.CharField(max_length=500)
    target_audience = models.CharField(
        max_length=20,
        choices=TargetAudience.choices,
        default=TargetAudience.BOTH
    )
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.occasion})"
