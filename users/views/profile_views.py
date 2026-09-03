from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.s3_utils import get_file_url
from users.serializers.user_serializers import UserProfileDetailSerializer
from users.services.auth_services import get_tokens_for_user
from users.services.email_service import send_welcome_email
from users.services.profile_service import create_user_profile


class CreateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        success, result, is_created = create_user_profile(request.user, request.data)

        if not success:
            return Response(
                {
                    "success": False,
                    "errors": result
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        msg = "Profile created successfully." if is_created else "Profile updated successfully."
        status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK

        if is_created:
            try:
                send_welcome_email(request.user)
            except Exception:
                pass

        main_tokens = get_tokens_for_user(request.user, is_temp=False)

        return Response(
            {
                "success": True,
                "message": msg,
                "tokens": main_tokens,
                "is_profile_created": True
            },
            status=status_code
        )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        profile_picture = None
        if user.user_type == 'creator' and hasattr(user, 'creator_profile') and user.creator_profile:
            profile_picture = user.creator_profile.profile_picture
        elif user.user_type == 'learner' and hasattr(user, 'learner_profile') and user.learner_profile:
            profile_picture = user.learner_profile.profile_picture

        is_profile_created = bool(
            (user.user_type == 'creator' and hasattr(user, 'creator_profile') and user.creator_profile) or
            (user.user_type == 'learner' and hasattr(user, 'learner_profile') and user.learner_profile)
        )

        return Response(
            {
                "success": True,
                "user": {
                    "name": user.full_name,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "profile_picture": get_file_url(profile_picture),
                    "user_type": user.user_type,
                    "is_profile_created": is_profile_created
                }
            },
            status=status.HTTP_200_OK
        )


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileDetailSerializer(request.user)
        return Response(
            {
                "success": True,
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        serializer = UserProfileDetailSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Profile updated successfully."
            },
            status=status.HTTP_200_OK
        )
