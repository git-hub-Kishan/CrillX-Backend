import re
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.helpers.model_helpers import SignupType, UserType
from users.services.auth_services import check_email_status, register_new_user, validate_phone_number, verify_google_oauth_token, validate_password_strength
from users.services.otp_service import (
    create_and_send_forgot_password_otp,
    create_and_send_user_otp,
    resend_user_otp,
    reset_user_password,
    verify_forgot_password_otp,
    verify_user_otp,
)
from users.services.email_service import send_password_changed_alert

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'phone_number',
            'user_type',
            'signup_type',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        email = attrs.get('email')
        exists, is_verified, _ = check_email_status(email)
        if exists and is_verified:
            raise serializers.ValidationError({"email": "User with this email already exists."})

        phone_number = attrs.get('phone_number')
        if phone_number:
            is_valid_phone, phone_error = validate_phone_number(phone_number, email)
            if not is_valid_phone:
                raise serializers.ValidationError({"phone_number": phone_error})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        signup_type = validated_data.get('signup_type', SignupType.EMAIL)

        user = register_new_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            user_type=validated_data.get('user_type', UserType.LEARNER),
            signup_type=signup_type,
        )

        if signup_type == SignupType.EMAIL:
            create_and_send_user_otp(user)

        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        is_valid, error_msg, user = verify_user_otp(email, otp)
        if not is_valid:
            raise serializers.ValidationError({"otp": error_msg})

        attrs['user'] = user
        return attrs


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(choices=UserType.choices, default=UserType.LEARNER, required=False)

    def validate(self, attrs):
        id_token = attrs.get('id_token')
        google_config = verify_google_oauth_token(id_token)
        attrs['google_config'] = google_config
        return attrs


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        success, message, user = resend_user_otp(email)
        if not success:
            raise serializers.ValidationError({"email": message})

        attrs['user'] = user
        attrs['message'] = message
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        if not getattr(user, 'is_active', True):
            raise serializers.ValidationError({"email": "Your account is deactivated. Please contact support."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid email or password."})

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        user = self.context.get('request').user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Wrong old password."})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})

        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})

        return attrs

    def save(self, **kwargs):
        user = self.context.get('request').user
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        send_password_changed_alert(user)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        if not getattr(user, 'is_active', True):
            raise serializers.ValidationError({"email": "Your account is deactivated. Please contact support."})

        if not user.is_verified:
            raise serializers.ValidationError({"email": "Your account is not verified. Please verify your account first."})

        attrs['user'] = user
        return attrs


class VerifyForgotPasswordOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        otp = attrs.get('otp')

        is_valid, error_msg, user = verify_forgot_password_otp(email, otp)
        if not is_valid:
            raise serializers.ValidationError({"otp": error_msg})

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        return validate_password_strength(value)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        email = attrs.get('email', '').strip().lower()
        otp = attrs.get('otp')

        is_valid, error_msg, user = verify_forgot_password_otp(email, otp)
        if not is_valid:
            raise serializers.ValidationError({"otp": error_msg})

        if user.check_password(password):
            raise serializers.ValidationError({"password": "New password cannot be the same as your last few passwords."})

        attrs['user'] = user
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            data = {
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            }
            attrs['tokens'] = data
            return attrs
        except Exception:
            raise serializers.ValidationError({"refresh_token": "Invalid or expired refresh token."})


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()
            return attrs
        except Exception:
            raise serializers.ValidationError({"refresh_token": "Invalid or expired refresh token."})

