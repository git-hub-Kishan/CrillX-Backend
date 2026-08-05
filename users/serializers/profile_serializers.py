from rest_framework import serializers
from users.models import CreatorProfile, LearnerProfile
from users.helpers.location_helpers import State
from users.helpers.model_helpers import ExperienceRange, Profession, TeachingCategory


class CreatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorProfile
        fields = [
            'id',
            'profile_picture',
            'yt_username',
            'insta_username',
            'dob',
            'state',
            'city',
            'teaching_category',
            'experience',
            'profession',
            'bio',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_state(self, value):
        if value and value not in State.values:
            raise serializers.ValidationError(f"Invalid state code. Choose from: {State.values}")
        return value

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


class LearnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProfile
        fields = [
            'id',
            'profile_picture',
            'dob',
            'state',
            'city',
            'profession',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_state(self, value):
        if value and value not in State.values:
            raise serializers.ValidationError(f"Invalid state code. Choose from: {State.values}")
        return value

    def validate_profession(self, value):
        if value and value not in Profession.values:
            raise serializers.ValidationError(f"Invalid profession. Choose from: {Profession.values}")
        return value
