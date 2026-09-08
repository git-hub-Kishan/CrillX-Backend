from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import StandardResultsSetPagination
from utils.permissions import IsSuperAdminUser
from courses.serializers.course_serializers import CourseModuleSerializer
from admin.serializers.creator_serializers import (
    AdminCreatorListSerializer,
    AdminCreatorDetailSerializer,
    AdminCreatorCourseSerializer,
)
from admin.services.creator_services import (
    get_admin_creators_queryset,
    get_admin_creator_by_identifier,
    get_admin_creator_courses_queryset,
    get_admin_course_by_identifier,
    get_admin_course_modules_queryset,
)


class AdminCreatorListAPIView(APIView):
    """
    Admin API endpoint to list creators with pagination, search, and status filter.
    GET /admin/users/creators/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search') or request.query_params.get('q')
        status_query = request.query_params.get('status')
        is_active_query = request.query_params.get('is_active')
        is_verified_query = request.query_params.get('is_verified')

        queryset = get_admin_creators_queryset(
            search=search_query,
            status=status_query,
            is_active=is_active_query,
            is_verified=is_verified_query,
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = AdminCreatorListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AdminCreatorListSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminCreatorDetailAPIView(APIView):
    """
    Admin API endpoint to get complete personal profile details of a creator by ID or UUID.
    GET /admin/users/creators/<creator_identifier>/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, creator_identifier, *args, **kwargs):
        creator = get_admin_creator_by_identifier(creator_identifier)
        if not creator:
            return Response(
                {
                    "success": False,
                    "message": "Creator not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminCreatorDetailSerializer(creator)
        return Response(
            {
                "success": True,
                "creator": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminCreatorCoursesAPIView(APIView):
    """
    Admin API endpoint to list all courses created by a specific creator with search, filters, module count and pagination.
    GET /admin/users/creators/<creator_identifier>/courses/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, creator_identifier, *args, **kwargs):
        creator = get_admin_creator_by_identifier(creator_identifier)
        if not creator:
            return Response(
                {
                    "success": False,
                    "message": "Creator not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        search_query = request.query_params.get('search') or request.query_params.get('q')
        language_query = request.query_params.get('language') or request.query_params.get('lang')
        status_query = request.query_params.get('status')
        min_price_query = request.query_params.get('min_price')
        max_price_query = request.query_params.get('max_price')

        queryset = get_admin_creator_courses_queryset(
            creator=creator,
            search=search_query,
            language=language_query,
            status_param=status_query,
            min_price=min_price_query,
            max_price=max_price_query,
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = AdminCreatorCourseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AdminCreatorCourseSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AdminCreatorCourseModulesAPIView(APIView):
    """
    Admin API endpoint to list all modules of a specific course with search and pagination.
    GET /admin/users/creators/<creator_identifier>/courses/<course_identifier>/modules/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, creator_identifier, course_identifier, *args, **kwargs):
        creator = get_admin_creator_by_identifier(creator_identifier)
        if not creator:
            return Response(
                {
                    "success": False,
                    "message": "Creator not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        course = get_admin_course_by_identifier(course_identifier, creator=creator)
        if not course:
            return Response(
                {
                    "success": False,
                    "message": "Course not found for this creator."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        search_query = request.query_params.get('search') or request.query_params.get('q')
        modules_queryset = get_admin_course_modules_queryset(course, search=search_query)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(modules_queryset, request, view=self)

        if page is not None:
            serializer = CourseModuleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CourseModuleSerializer(modules_queryset, many=True)
        return Response(
            {
                "success": True,
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )
