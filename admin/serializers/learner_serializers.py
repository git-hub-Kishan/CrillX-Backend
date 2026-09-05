from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.s3_utils import get_file_url

User = get_user_model()


class AdminLearnerListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing learners in the admin panel.
    Returns: uuid, name, profile_picture, profession, is_active, is_verified.
    """

    class Meta:
        model = User
        fields = [
            'uuid',
            'is_active',
            'is_verified',
        ]

    def to_representation(self, instance):
        profile = getattr(instance, 'learner_profile', None)

        # Profile Picture (S3 resolution logic)
        profile_picture = None
        if profile and profile.profile_picture:
            profile_picture = get_file_url(profile.profile_picture)

        return {
            "uuid": str(instance.uuid),
            "name": instance.full_name or instance.username,
            "profile_picture": profile_picture,
            "profession": profile.profession if profile else None,
            "is_active": instance.is_active,
            "is_verified": instance.is_verified,
        }
