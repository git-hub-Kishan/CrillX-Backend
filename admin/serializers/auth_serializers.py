from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.helpers.model_helpers import UserType

User = get_user_model()


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        # Ensure user is an administrator
        is_admin = (
            user.user_type == UserType.SUPERADMIN or 
            user.is_superuser or 
            user.is_staff
        )
        if not is_admin:
            raise serializers.ValidationError({"email": "Access denied. You do not have administrator permissions."})

        if not getattr(user, 'is_active', True):
            raise serializers.ValidationError({"email": "Your account is deactivated. Please contact support."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid email or password."})

        attrs['user'] = user
        return attrs
