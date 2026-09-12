import logging
from typing import Optional, Tuple
from django.db.models import Q
from django.utils import timezone

from admin.models import HeaderGIFBanner
from admin.helpers.banner_helpers import TargetAudience, BannerStatus
from users.helpers.model_helpers import UserType
from users.services.s3_services import delete_file_from_s3

logger = logging.getLogger(__name__)


def get_header_gifs_queryset(search: Optional[str] = None, status: Optional[str] = None, target_audience: Optional[str] = None):
    """
    Returns filtered queryset for header GIF banners based on search query, dynamic status, and target audience.
    """
    queryset = HeaderGIFBanner.objects.all()
    now = timezone.now()

    if search:
        search = search.strip()
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(occasion__icontains=search)
        )

    if target_audience and target_audience.lower() in [TargetAudience.BOTH, TargetAudience.CREATORS, TargetAudience.LEARNERS]:
        queryset = queryset.filter(target_audience=target_audience.lower())

    if status:
        status_clean = status.strip().lower()
        if status_clean == BannerStatus.ACTIVE:
            queryset = queryset.filter(
                is_active=True,
                start_date_time__lte=now,
                end_date_time__gte=now
            )
        elif status_clean == BannerStatus.SCHEDULED:
            queryset = queryset.filter(
                is_active=True,
                start_date_time__gt=now
            )
        elif status_clean == BannerStatus.EXPIRED:
            queryset = queryset.filter(
                end_date_time__lt=now
            )
        elif status_clean == BannerStatus.INACTIVE:
            queryset = queryset.filter(
                is_active=False
            )

    return queryset.order_by('-created_at')


def get_header_gif_by_identifier(identifier: str) -> Optional[HeaderGIFBanner]:
    """
    Retrieves a header GIF banner by either primary key integer ID or UUID string.
    """
    if not identifier:
        return None

    try:
        if str(identifier).isdigit():
            return HeaderGIFBanner.objects.filter(id=int(identifier)).first()
        return HeaderGIFBanner.objects.filter(uuid=identifier).first()
    except Exception as e:
        logger.warning(f"Error querying HeaderGIFBanner by identifier {identifier}: {e}")
        return None


def create_header_gif(validated_data: dict) -> HeaderGIFBanner:
    """
    Creates and saves a new HeaderGIFBanner instance.
    """
    return HeaderGIFBanner.objects.create(**validated_data)


def update_header_gif(instance: HeaderGIFBanner, validated_data: dict) -> HeaderGIFBanner:
    """
    Updates an existing HeaderGIFBanner instance with validated fields.
    """
    for key, value in validated_data.items():
        setattr(instance, key, value)
    instance.save()
    return instance


def delete_header_gif(instance: HeaderGIFBanner) -> Tuple[bool, str]:
    """
    Deletes the HeaderGIFBanner instance and cleans up associated S3 file if present.
    """
    try:
        if instance.file_key:
            try:
                delete_file_from_s3(instance.file_key)
            except Exception as e:
                logger.warning(f"Failed to delete S3 file {instance.file_key} during banner deletion: {e}")

        instance.delete()
        return True, "Header GIF banner deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting HeaderGIFBanner {instance.id}: {e}")
        return False, str(e)


def get_active_header_gif_for_client(audience: Optional[str] = None, user=None) -> Optional[HeaderGIFBanner]:
    """
    Returns the currently active Header GIF banner for a given client context.
    Matches active banners where is_active=True and start_date_time <= now <= end_date_time.
    """
    now = timezone.now()

    effective_audience = audience.lower() if audience else None

    if not effective_audience and user and user.is_authenticated:
        if getattr(user, 'user_type', None) == UserType.CREATOR:
            effective_audience = TargetAudience.CREATORS
        elif getattr(user, 'user_type', None) == UserType.LEARNER:
            effective_audience = TargetAudience.LEARNERS

    if effective_audience in [TargetAudience.CREATORS, TargetAudience.LEARNERS]:
        allowed_audiences = [effective_audience, TargetAudience.BOTH]
    else:
        allowed_audiences = [TargetAudience.BOTH, TargetAudience.CREATORS, TargetAudience.LEARNERS]

    active_banner = HeaderGIFBanner.objects.filter(
        is_active=True,
        start_date_time__lte=now,
        end_date_time__gte=now,
        target_audience__in=allowed_audiences
    ).order_by('-start_date_time', '-created_at').first()

    return active_banner
