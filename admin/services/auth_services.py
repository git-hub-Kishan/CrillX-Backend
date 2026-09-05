from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_admin(user):
    """
    Generate JWT access and refresh tokens for an admin user.
    Also updates user's last_login timestamp.
    """
    update_last_login(None, user)
    refresh = RefreshToken.for_user(user)

    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }
