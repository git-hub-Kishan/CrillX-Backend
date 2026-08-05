import re
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from users.helpers.model_helpers import SignupType, UserType

User = get_user_model()


def validate_password_strength(value):
    """
    Validates that a password meets the required strength rules:
    - Min 8 chars
    - 1 uppercase, 1 lowercase
    - 1 number
    - 1 special character
    """
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', value):
        raise serializers.ValidationError("Password must contain at least one number.")
    if not re.search(r'[^A-Za-z0-9]', value):
        raise serializers.ValidationError("Password must contain at least one special character.")
    return value


def check_email_status(email):
    user = User.objects.filter(email__iexact=email.strip()).first()
    if user:
        return True, user.is_verified, user
    return False, False, None


def validate_phone_number(phone_number, email):
    if not phone_number:
        return True, None

    phone = phone_number.strip()
    existing_user = User.objects.filter(phone_number=phone).exclude(email__iexact=email.strip()).first()
    if existing_user:
        return False, "This phone number is already associated with another account."

    return True, None


def register_new_user(first_name, last_name, email, password, phone_number=None, user_type=UserType.LEARNER, signup_type=SignupType.EMAIL):
    email_clean = email.strip().lower()
    user = User.objects.filter(email__iexact=email_clean).first()

    if not user:
        user = User(
            username=email_clean,
            email=email_clean,
        )

    user.first_name = first_name.strip()
    user.last_name = last_name.strip()
    user.phone_number = phone_number.strip() if phone_number else None
    user.user_type = user_type
    user.signup_type = signup_type
    user.is_verified = False
    user.set_password(password)
    user.save()

    return user


def is_user_profile_created(user):
    """
    Check if the user has completed their profile setup based on user_type.
    """
    if user.user_type == UserType.CREATOR:
        return hasattr(user, 'creator_profile') and user.creator_profile is not None
    elif user.user_type == UserType.LEARNER:
        return hasattr(user, 'learner_profile') and user.learner_profile is not None
    return True


def get_tokens_for_user(user, is_temp=False):
    """
    Returns JWT access and refresh tokens.
    If is_temp is True (profile not created yet), returns temporary access token with short expiry and no main refresh token.
    Updates last_login timestamp for the user.
    """
    from datetime import timedelta
    from django.contrib.auth.models import update_last_login
    from rest_framework_simplejwt.tokens import RefreshToken

    update_last_login(None, user)

    refresh = RefreshToken.for_user(user)

    if is_temp:
        refresh['is_temp'] = True
        refresh.access_token['is_temp'] = True
        refresh.access_token.set_exp(lifetime=timedelta(minutes=30))
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': None,
        }

    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }


def handle_google_user(email, first_name='', last_name='', user_type=UserType.LEARNER):
    email_clean = email.strip().lower()
    user = User.objects.filter(email__iexact=email_clean).first()

    if not user:
        user = User(
            username=email_clean,
            email=email_clean,
            signup_type=SignupType.GOOGLE,
            user_type=user_type,
            is_verified=True,
        )
        user.set_unusable_password()

    if first_name and not user.first_name:
        user.first_name = first_name.strip()
    if last_name and not user.last_name:
        user.last_name = last_name.strip()

    user.is_verified = True
    user.save()
    return user


def verify_google_oauth_token(token_string):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    return {
        'client_id_configured': bool(client_id),
        'client_secret_configured': bool(client_secret),
    }
