from django.utils import timezone
from rest_framework import serializers
from admin.models import HeaderGIFBanner
from admin.helpers.banner_helpers import TargetAudience, BannerStatus
from utils.s3_utils import get_file_url


class HeaderGIFListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing GIF banners in the admin management table.
    """
    status = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = HeaderGIFBanner
        fields = [
            'id',
            'uuid',
            'title',
            'occasion',
            'target_audience',
            'preview_url',
            'start_date_time',
            'end_date_time',
            'is_active',
            'status',
            'created_at',
            'updated_at',
        ]

    def get_status(self, obj):
        now = timezone.now()
        if not obj.is_active:
            return BannerStatus.INACTIVE
        if now < obj.start_date_time:
            return BannerStatus.SCHEDULED
        if obj.start_date_time <= now <= obj.end_date_time:
            return BannerStatus.ACTIVE
        return BannerStatus.EXPIRED

    def get_preview_url(self, obj):
        return get_file_url(obj.file_key)


class HeaderGIFDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving details of a single GIF banner.
    """
    status = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = HeaderGIFBanner
        fields = [
            'id',
            'uuid',
            'title',
            'occasion',
            'target_audience',
            'preview_url',
            'start_date_time',
            'end_date_time',
            'is_active',
            'status',
            'created_at',
            'updated_at',
        ]

    def get_status(self, obj):
        now = timezone.now()
        if not obj.is_active:
            return BannerStatus.INACTIVE
        if now < obj.start_date_time:
            return BannerStatus.SCHEDULED
        if obj.start_date_time <= now <= obj.end_date_time:
            return BannerStatus.ACTIVE
        return BannerStatus.EXPIRED

    def get_preview_url(self, obj):
        return get_file_url(obj.file_key)


class HeaderGIFCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating a Header GIF banner.
    """
    target_audience = serializers.ChoiceField(
        choices=TargetAudience.choices,
        default=TargetAudience.BOTH
    )

    class Meta:
        model = HeaderGIFBanner
        fields = [
            'title',
            'occasion',
            'target_audience',
            'file_key',
            'start_date_time',
            'end_date_time',
            'is_active',
        ]

    def validate(self, attrs):
        start_date_time = attrs.get('start_date_time')
        end_date_time = attrs.get('end_date_time')

        if self.instance:
            if start_date_time is None:
                start_date_time = self.instance.start_date_time
            if end_date_time is None:
                end_date_time = self.instance.end_date_time

        if start_date_time and end_date_time and end_date_time <= start_date_time:
            raise serializers.ValidationError({
                "end_date_time": "End date & time must be after the start date & time."
            })

        return attrs


class ActiveHeaderGIFResponseSerializer(serializers.ModelSerializer):
    """
    Public/Client serializer for rendering the active header GIF banner.
    """
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = HeaderGIFBanner
        fields = [
            'id',
            'uuid',
            'title',
            'occasion',
            'target_audience',
            'file_url',
            'start_date_time',
            'end_date_time',
        ]

    def get_file_url(self, obj):
        return get_file_url(obj.file_key)
