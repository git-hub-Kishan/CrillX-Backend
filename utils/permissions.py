from rest_framework.permissions import BasePermission
from users.helpers.model_helpers import UserType


class IsCreatorUser(BasePermission):
    """
    Custom permission to only allow users with user_type 'creator' to access.
    """
    message = "Only creators are allowed to perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.user_type == UserType.CREATOR
        )


class IsLearnerUser(BasePermission):
    """
    Custom permission to only allow users with user_type 'learner' to access.
    """
    message = "Only learners are allowed to perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.user_type == UserType.LEARNER
        )
