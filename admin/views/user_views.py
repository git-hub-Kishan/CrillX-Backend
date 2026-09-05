from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsSuperAdminUser
from admin.services.user_services import get_user_kpis, toggle_user_status


class AdminUserKPIAPIView(APIView):
    """
    Admin API endpoint to retrieve high-level user KPI metrics.
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, *args, **kwargs):
        stats = get_user_kpis()
        return Response(
            {
                "success": True,
                "stats": stats
            },
            status=status.HTTP_200_OK
        )


class AdminUserStatusUpdateAPIView(APIView):
    """
    Admin API endpoint to toggle / update active status for a single user or multiple users.
    Payload options:
      - Single: { "user_uuid": "..." } or { "user_id": "..." }
      - Bulk: { "user_uuids": ["...", "..."] } or { "user_ids": [...] }
      - Optional override: { "is_active": false }
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def _extract_identifiers(self, data):
        if 'user_uuids' in data:
            return data['user_uuids']
        if 'uuids' in data:
            return data['uuids']
        if 'user_uuid' in data:
            return [data['user_uuid']]
        if 'uuid' in data:
            return [data['uuid']]
        if 'user_ids' in data:
            return data['user_ids']
        if 'ids' in data:
            return data['ids']
        if 'user_id' in data:
            return [data['user_id']]
        if 'id' in data:
            return [data['id']]
        return []

    def patch(self, request, *args, **kwargs):
        return self._handle_status_update(request)

    def post(self, request, *args, **kwargs):
        return self._handle_status_update(request)

    def _handle_status_update(self, request):
        data = request.data
        identifiers = self._extract_identifiers(data)

        if not identifiers:
            return Response(
                {
                    "success": False,
                    "errors": {"user_uuid": "Please provide user_uuid or user_uuids."}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        is_active_override = data.get('is_active')

        success, result = toggle_user_status(
            user_identifiers=identifiers,
            current_admin_user=request.user,
            is_active_override=is_active_override
        )

        if not success:
            return Response(
                {
                    "success": False,
                    "errors": {"detail": result}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": f"Successfully updated status for {len(result)} user(s).",
                "updated_count": len(result),
                "users": result
            },
            status=status.HTTP_200_OK
        )
