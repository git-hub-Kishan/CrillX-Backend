from django.db import models
from django.utils import timezone


class TargetAudience(models.TextChoices):
    BOTH = 'both', 'Both (Creators & Learners)'
    CREATORS = 'creators', 'Creators only'
    LEARNERS = 'learners', 'Learners only'


class BannerStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    SCHEDULED = 'scheduled', 'Scheduled'
    EXPIRED = 'expired', 'Expired'
    INACTIVE = 'inactive', 'Inactive'


def calculate_banner_status(is_active: bool, start_date_time, end_date_time, now=None):
    """
    Computes the banner status dynamically based on current time and active flag.
    """
    if now is None:
        now = timezone.now()

    if not is_active:
        return BannerStatus.INACTIVE

    if now < start_date_time:
        return BannerStatus.SCHEDULED

    if start_date_time <= now <= end_date_time:
        return BannerStatus.ACTIVE

    return BannerStatus.EXPIRED
