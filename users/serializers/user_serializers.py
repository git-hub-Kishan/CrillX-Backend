from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.s3_utils import get_file_url
from users.helpers.model_helpers import ExperienceRange, Profession, TeachingCategory, UserType
from users.serializers.profile_serializers import CreatorProfileSerializer, LearnerProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for representing User model instance, including serializer-level computed is_profile_created and profile data.
    """
    full_name = serializers.CharField(read_only=True)
    is_profile_created = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'signup_type',
            'user_type',
            'is_verified',
            'is_profile_created',
            'profile',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid', 'is_verified', 'is_profile_created', 'profile', 'created_at', 'updated_at']

    def get_is_profile_created(self, obj):
        if obj.user_type == UserType.CREATOR:
            return hasattr(obj, 'creator_profile') and obj.creator_profile is not None
        elif obj.user_type == UserType.LEARNER:
            return hasattr(obj, 'learner_profile') and obj.learner_profile is not None
        return True

    def get_profile(self, obj):
        if obj.user_type == UserType.CREATOR and hasattr(obj, 'creator_profile') and obj.creator_profile:
            return CreatorProfileSerializer(obj.creator_profile).data
        elif obj.user_type == UserType.LEARNER and hasattr(obj, 'learner_profile') and obj.learner_profile:
            return LearnerProfileSerializer(obj.learner_profile).data
        return None


class UserProfileDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    user_type = serializers.CharField(read_only=True)

    # State and City are strictly read-only (cannot be updated)
    state = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)

    # Updatable user fields
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # Updatable profile fields
    profile_picture = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dob = serializers.DateField(required=False, allow_null=True)
    profession = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # Creator-specific updatable fields
    teaching_category = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    experience = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    yt_username = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    insta_username = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_teaching_category(self, value):
        if value and value not in TeachingCategory.values:
            raise serializers.ValidationError(f"Invalid teaching category. Choose from: {TeachingCategory.values}")
        return value

    def validate_experience(self, value):
        if value and value not in ExperienceRange.values:
            raise serializers.ValidationError(f"Invalid experience range. Choose from: {ExperienceRange.values}")
        return value

    def validate_profession(self, value):
        if value and value not in Profession.values:
            raise serializers.ValidationError(f"Invalid profession. Choose from: {Profession.values}")
        return value

    def validate_yt_username(self, value):
        from users.helpers.model_helpers import standardize_youtube_url
        return standardize_youtube_url(value)

    def validate_insta_username(self, value):
        from users.helpers.model_helpers import standardize_instagram_url
        return standardize_instagram_url(value)


    def to_representation(self, instance):
        user = instance
        profile = None

        if user.user_type == UserType.CREATOR and hasattr(user, 'creator_profile') and user.creator_profile:
            profile = user.creator_profile
        elif user.user_type == UserType.LEARNER and hasattr(user, 'learner_profile') and user.learner_profile:
            profile = user.learner_profile

        data = {
            "uuid": str(user.uuid),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "user_type": user.user_type,
            "profile_picture": get_file_url(profile.profile_picture) if (profile and profile.profile_picture) else None,
            "dob": profile.dob.isoformat() if (profile and profile.dob) else None,
            "state": profile.state if profile else None,
            "city": profile.city if profile else None,
            "profession": profile.profession if profile else None,
        }

        if user.user_type == UserType.CREATOR:
            data.update({
                "teaching_category": profile.teaching_category if profile else None,
                "experience": profile.experience if profile else None,
                "yt_username": profile.yt_username if profile else None,
                "insta_username": profile.insta_username if profile else None,
                "bio": profile.bio if profile else None,
            })

        return data

    def update(self, instance, validated_data):
        user = instance

        # 1. Update User model fields
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
        if 'phone_number' in validated_data:
            user.phone_number = validated_data['phone_number']

        user.save()

        # 2. Update Creator/Learner Profile fields
        if user.user_type == UserType.CREATOR and hasattr(user, 'creator_profile') and user.creator_profile:
            profile = user.creator_profile
            creator_fields = ['profile_picture', 'dob', 'profession', 'teaching_category', 'experience', 'yt_username', 'insta_username', 'bio']
            for field in creator_fields:
                if field in validated_data:
                    setattr(profile, field, validated_data[field])
            profile.save()

        elif user.user_type == UserType.LEARNER and hasattr(user, 'learner_profile') and user.learner_profile:
            profile = user.learner_profile
            learner_fields = ['profile_picture', 'dob', 'profession']
            for field in learner_fields:
                if field in validated_data:
                    setattr(profile, field, validated_data[field])
            profile.save()

        return user


