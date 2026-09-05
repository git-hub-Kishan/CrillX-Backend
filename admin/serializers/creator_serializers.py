from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.s3_utils import get_file_url

User = get_user_model()


class AdminCreatorListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing creators in the admin panel.
    Returns: uuid, name, profile_picture, teaching_category, yt_link, insta_link, is_active, is_verified.
    """

    class Meta:
        model = User
        fields = [
            'uuid',
            'is_active',
            'is_verified',
        ]

    def to_representation(self, instance):
        profile = getattr(instance, 'creator_profile', None)

        # YouTube Link
        yt_link = None
        if profile and profile.yt_username:
            username = profile.yt_username.strip()
            if username.startswith('http://') or username.startswith('https://'):
                yt_link = username
            else:
                clean_handle = username.lstrip('@')
                yt_link = f"https://www.youtube.com/@{clean_handle}" if clean_handle else None

        # Instagram Link
        insta_link = None
        if profile and profile.insta_username:
            username = profile.insta_username.strip()
            if username.startswith('http://') or username.startswith('https://'):
                insta_link = username
            else:
                clean_handle = username.lstrip('@')
                insta_link = f"https://www.instagram.com/{clean_handle}" if clean_handle else None

        # Profile Picture (S3 resolution logic)
        profile_picture = None
        if profile and profile.profile_picture:
            profile_picture = get_file_url(profile.profile_picture)

        return {
            "uuid": str(instance.uuid),
            "name": instance.full_name or instance.username,
            "profile_picture": profile_picture,
            "teaching_category": profile.teaching_category if profile else None,
            "yt_link": yt_link,
            "insta_link": insta_link,
            "is_active": instance.is_active,
            "is_verified": instance.is_verified,
        }
