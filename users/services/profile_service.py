from users.helpers.model_helpers import UserType
from users.models import CreatorProfile, LearnerProfile
from users.serializers.profile_serializers import CreatorProfileSerializer, LearnerProfileSerializer


def create_or_update_creator_profile(user, data):
    """
    Service helper to validate & create/update a CreatorProfile for a given user.
    """
    profile = getattr(user, 'creator_profile', None)
    serializer = CreatorProfileSerializer(instance=profile, data=data, partial=True)
    if not serializer.is_valid():
        return False, serializer.errors, None

    creator_profile, created = CreatorProfile.objects.update_or_create(
        user=user,
        defaults=serializer.validated_data
    )
    return True, CreatorProfileSerializer(creator_profile).data, created


def create_or_update_learner_profile(user, data):
    """
    Service helper to validate & create/update a LearnerProfile for a given user.
    """
    profile = getattr(user, 'learner_profile', None)
    serializer = LearnerProfileSerializer(instance=profile, data=data, partial=True)
    if not serializer.is_valid():
        return False, serializer.errors, None

    learner_profile, created = LearnerProfile.objects.update_or_create(
        user=user,
        defaults=serializer.validated_data
    )
    return True, LearnerProfileSerializer(learner_profile).data, created


def create_user_profile(user, data):
    """
    Common entry point to create/update profile based on user's registered user_type.
    """
    if user.user_type == UserType.CREATOR:
        return create_or_update_creator_profile(user, data)
    else:
        return create_or_update_learner_profile(user, data)
