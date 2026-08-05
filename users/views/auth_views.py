from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.auth_serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    GoogleLoginSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
    VerifyForgotPasswordOTPSerializer,
    VerifyOTPSerializer,
)
from users.serializers.user_serializers import UserSerializer
from users.services.auth_services import get_tokens_for_user, handle_google_user, is_user_profile_created
from users.services.otp_service import create_and_send_forgot_password_otp, create_and_send_user_otp, reset_user_password




class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        msg = "User registered successfully. Please verify your OTP to continue." if user.signup_type == 'email' else "User registered successfully."
        requires_otp = (user.signup_type == 'email' and not user.is_verified)

        return Response(
            {
                "success": True,
                "message": msg,
                "requires_otp_verification": requires_otp
            },
            status=status.HTTP_201_CREATED
        )


class VerifyOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        is_created = is_user_profile_created(user)
        tokens = get_tokens_for_user(user, is_temp=not is_created)
        user_data = UserSerializer(user).data

        return Response(
            {
                "success": True,
                "message": "OTP verified successfully.",
                "tokens": tokens,
                "user_type": user.user_type,
                "full_name": user.full_name,
                "is_profile_created": is_created
            },
            status=status.HTTP_200_OK
        )


class ResendOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": serializer.validated_data.get('message', "A new OTP code has been sent to your email.")
            },
            status=status.HTTP_200_OK
        )


class GoogleLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GoogleLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.data.get('email', 'google.user@example.com')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        user_type = serializer.validated_data.get('user_type')

        user, success = handle_google_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )

        if not success or not user:
            return Response(
                {
                    "success": False,
                    "account_not_found": True,
                    "message": "No account found with this Google email. Please register first as a Learner or Creator."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        is_created = is_user_profile_created(user)
        tokens = get_tokens_for_user(user, is_temp=not is_created)
        user_data = UserSerializer(user).data

        return Response(
            {
                "success": True,
                "message": "Google authentication successful.",
                "tokens": tokens,
                "user_type": user.user_type,
                "full_name": user.full_name,
                "is_profile_created": is_created
            },
            status=status.HTTP_200_OK
        )


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']

        if not user.is_verified:
            create_and_send_user_otp(user)
            return Response(
                {
                    "success": False,
                    "message": "Your email address is not verified. A new OTP code has been sent.",
                    "requires_otp_verification": True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        is_created = is_user_profile_created(user)
        tokens = get_tokens_for_user(user, is_temp=not is_created)
        user_data = UserSerializer(user).data

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "tokens": tokens,
                "user_type": user.user_type,
                "full_name": user.full_name,
                "is_profile_created": is_created
            },
            status=status.HTTP_200_OK
        )


class RefreshTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'refresh' in data and 'refresh_token' not in data:
            data['refresh_token'] = data['refresh']

        serializer = RefreshTokenSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Token refreshed successfully.",
                "tokens": serializer.validated_data['tokens']
            },
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'refresh' in data and 'refresh_token' not in data:
            data['refresh_token'] = data['refresh']

        serializer = LogoutSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Successfully logged out."
            },
            status=status.HTTP_200_OK
        )


class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        create_and_send_forgot_password_otp(user)

        return Response(
            {
                "success": True,
                "message": "Password reset OTP sent to your email."
            },
            status=status.HTTP_200_OK
        )


class VerifyForgotPasswordOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyForgotPasswordOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "OTP verified successfully. You can now reset your password."
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        password = serializer.validated_data['password']

        success, message = reset_user_password(user, password)
        if not success:
            return Response(
                {
                    "success": False,
                    "errors": {"password": message}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": message
            },
            status=status.HTTP_200_OK
        )


class ChangePasswordAPIView(APIView):
    from rest_framework.permissions import IsAuthenticated
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Password changed successfully."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An error occurred while changing password.",
                    "errors": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


