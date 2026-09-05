from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admin.serializers.auth_serializers import AdminLoginSerializer
from admin.services.auth_services import get_tokens_for_admin


class AdminLoginAPIView(APIView):
    """
    Admin Login endpoint using email and password only.
    Restricted to superadmin / superuser / staff accounts.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        tokens = get_tokens_for_admin(user)

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "tokens": tokens,
                "user_type": user.user_type,
                "full_name": user.full_name,
                "is_profile_created": True
            },
            status=status.HTTP_200_OK
        )
