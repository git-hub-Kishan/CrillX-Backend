from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import StandardResultsSetPagination
from utils.permissions import IsSuperAdminUser
from admin.serializers.learner_serializers import AdminLearnerListSerializer
from admin.services.learner_services import get_admin_learners_queryset


class AdminLearnerListAPIView(APIView):
    """
    Admin API endpoint to list learners with pagination, search, and status filter.
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search') or request.query_params.get('q')
        status_query = request.query_params.get('status')
        is_active_query = request.query_params.get('is_active')
        is_verified_query = request.query_params.get('is_verified')

        queryset = get_admin_learners_queryset(
            search=search_query,
            status=status_query,
            is_active=is_active_query,
            is_verified=is_verified_query,
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = AdminLearnerListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AdminLearnerListSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )
