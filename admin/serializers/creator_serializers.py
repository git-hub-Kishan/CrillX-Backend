from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import CreatorCourse
from utils.s3_utils import get_file_url

User = get_user_model()


class AdminCreatorListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing creators in the admin panel table.
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

        return {
            "uuid": str(instance.uuid),
            "name": instance.full_name or instance.username,
            "profile_picture": get_file_url(profile.profile_picture) if (profile and profile.profile_picture) else None,
            "teaching_category": profile.teaching_category if profile else None,
            "yt_link": yt_link,
            "insta_link": insta_link,
            "is_active": instance.is_active,
            "is_verified": instance.is_verified,
        }


class AdminCreatorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for complete personal profile details of a creator for admin.
    """

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_verified',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        profile = getattr(instance, 'creator_profile', None)

        return {
            "uuid": str(instance.uuid),
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "full_name": instance.full_name or instance.username,
            "phone_number": instance.phone_number,
            "is_verified": instance.is_verified,
            "is_active": instance.is_active,
            "profile_picture": get_file_url(profile.profile_picture) if (profile and profile.profile_picture) else None,
            "dob": profile.dob.isoformat() if (profile and profile.dob) else None,
            "state": profile.state if profile else None,
            "city": profile.city if profile else None,
            "profession": profile.profession if profile else None,
            "teaching_category": profile.teaching_category if profile else None,
            "experience": profile.experience if profile else None,
            "yt_username": profile.yt_username if profile else None,
            "insta_username": profile.insta_username if profile else None,
            "bio": profile.bio if profile else None,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }


class AdminCreatorCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for listing creator courses with module count for admin panel.
    """
    status = serializers.SerializerMethodField()
    total_modules = serializers.SerializerMethodField()

    class Meta:
        model = CreatorCourse
        fields = [
            'uuid',
            'course_name',
            'description',
            'price',
            'course_language',
            'course_thumbnail',
            'is_published',
            'is_locked',
            'status',
            'total_modules',
            'created_at',
            'updated_at',
        ]

    def get_status(self, obj):
        if not obj.is_published:
            return 'draft'
        if obj.is_locked:
            return 'locked'
        return 'published'

    def get_total_modules(self, obj):
        if hasattr(obj, 'modules_count'):
            return obj.modules_count
        return obj.modules.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('course_thumbnail'):
            data['course_thumbnail'] = get_file_url(data['course_thumbnail'])
        return data
