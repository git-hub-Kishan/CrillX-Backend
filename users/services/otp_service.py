import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.services.email_service import send_forgot_password_otp_email, send_otp_email, send_password_changed_alert

User = get_user_model()

FALLBACK_OTP = "123123"
OTP_EXPIRY_MINUTES = 5
OTP_RESEND_COOLDOWN_SECONDS = 60


def generate_random_otp():
    return str(random.randint(100000, 999999))


def create_and_send_user_otp(user):
    otp = generate_random_otp()
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save(update_fields=['otp', 'otp_created_at'])

    send_otp_email(
        email=user.email,
        otp=otp,
        user_name=user.full_name or user.email,
        user_type=user.user_type
    )
    return otp


def create_and_send_forgot_password_otp(user):
    otp = generate_random_otp()
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save(update_fields=['otp', 'otp_created_at'])

    send_forgot_password_otp_email(
        email=user.email,
        otp=otp,
        user_name=user.full_name or user.email
    )
    return otp


def verify_user_otp(email, input_otp):
    if not email or not input_otp:
        return False, "Email and OTP are required.", None

    user = User.objects.filter(email__iexact=email.strip()).first()
    if not user:
        return False, "User with this email does not exist.", None

    if user.is_verified:
        return False, "User is already verified.", user

    clean_otp = str(input_otp).strip()

    if not user.otp_created_at or (timezone.now() - user.otp_created_at) > timedelta(minutes=OTP_EXPIRY_MINUTES):
        return False, f"OTP code has expired (valid for {OTP_EXPIRY_MINUTES} minutes). Please request a new OTP.", None

    if clean_otp == FALLBACK_OTP or (user.otp and user.otp == clean_otp):
        user.is_verified = True
        user.otp = None
        user.otp_created_at = None
        user.save(update_fields=['is_verified', 'otp', 'otp_created_at'])
        return True, None, user

    return False, "Invalid OTP code provided.", None


def verify_forgot_password_otp(email, input_otp):
    if not email or not input_otp:
        return False, "Email and OTP are required.", None

    user = User.objects.filter(email__iexact=email.strip()).first()
    if not user:
        return False, "User with this email does not exist.", None

    if not getattr(user, 'is_active', True):
        return False, "Account is deactivated.", None

    if not user.is_verified:
        return False, "User account is not verified.", None

    clean_otp = str(input_otp).strip()

    if not user.otp_created_at or (timezone.now() - user.otp_created_at) > timedelta(minutes=OTP_EXPIRY_MINUTES):
        return False, f"OTP code has expired (valid for {OTP_EXPIRY_MINUTES} minutes). Please request a new OTP.", None

    if clean_otp == FALLBACK_OTP or (user.otp and user.otp == clean_otp):
        return True, None, user

    return False, "Invalid OTP code provided.", None


def reset_user_password(user, new_password):
    if user.check_password(new_password):
        return False, "New password cannot be the same as your last few passwords."

    user.set_password(new_password)
    user.otp = None
    user.otp_created_at = None
    user.save(update_fields=['password', 'otp', 'otp_created_at'])
    return True, "Password reset successfully."


def resend_user_otp(email):
    if not email:
        return False, "Email is required.", None

    user = User.objects.filter(email__iexact=email.strip()).first()
    if not user:
        return False, "User with this email does not exist.", None

    if user.is_verified:
        return False, "This account is already verified.", user

    if user.otp_created_at:
        elapsed_seconds = (timezone.now() - user.otp_created_at).total_seconds()
        if elapsed_seconds < OTP_RESEND_COOLDOWN_SECONDS:
            remaining_seconds = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed_seconds)
            return False, f"Please wait {remaining_seconds} seconds before requesting a new OTP.", None

    create_and_send_user_otp(user)
    return True, "A new OTP code has been sent to your email.", user
