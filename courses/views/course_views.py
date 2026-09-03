from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import StandardResultsSetPagination
from utils.permissions import IsCreatorUser
from courses.serializers.course_serializers import CreatorCourseSerializer, CourseModuleSerializer
from courses.services.course_services import (
    create_course,
    get_user_courses_queryset,
    get_course,
    update_course,
    create_course_modules,
    get_course_modules_queryset,
)


class CreatorCourseAPIView(APIView):
    """
    API View for Creator Courses:
    - POST: Create a new course (restricted to creators only).
    - GET: Retrieve a paginated list of courses created by the logged-in user with optional search, language, status, and price range filters.
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCreatorUser()]
        return [IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        success, result = create_course(user=request.user, data=request.data)
        if not success:
            return Response(
                {
                    "success": False,
                    "errors": result
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Course created successfully.",
                "course": result
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search') or request.query_params.get('q')
        language_query = request.query_params.get('language') or request.query_params.get('lang')
        status_query = request.query_params.get('status')
        min_price_query = request.query_params.get('min_price')
        max_price_query = request.query_params.get('max_price')

        queryset = get_user_courses_queryset(
            user=request.user,
            search=search_query,
            language=language_query,
            status_param=status_query,
            min_price=min_price_query,
            max_price=max_price_query
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = CreatorCourseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CreatorCourseSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "courses": serializer.data
            },
            status=status.HTTP_200_OK
        )


class CreatorCourseDetailAPIView(APIView):
    """
    API View for a single Creator Course (by UUID):
    - GET: Retrieve the course details.
    - PATCH: Partially update one or more fields of the course.
    """
    permission_classes = [IsAuthenticated, IsCreatorUser]

    def get(self, request, course_uuid, *args, **kwargs):
        success, result = get_course(user=request.user, course_uuid=course_uuid)
        if not success:
            return Response(
                {"success": False, "errors": result},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"success": True, "course": result},
            status=status.HTTP_200_OK
        )

    def patch(self, request, course_uuid, *args, **kwargs):
        success, result = update_course(user=request.user, course_uuid=course_uuid, data=request.data)
        if not success:
            http_status = status.HTTP_404_NOT_FOUND if "detail" in result else status.HTTP_400_BAD_REQUEST
            return Response(
                {"success": False, "errors": result},
                status=http_status
            )
        return Response(
            {"success": True, "message": "Course updated successfully.", "course": result},
            status=status.HTTP_200_OK
        )


class CourseModuleListCreateAPIView(APIView):
    """
    API View for Course Modules (by course_uuid):
    - POST: Add one or multiple modules to a course owned by the logged-in creator.
    - GET: Retrieve a paginated list of all modules for a course with S3 URLs resolved.
    """
    permission_classes = [IsAuthenticated, IsCreatorUser]

    def post(self, request, course_uuid, *args, **kwargs):
        success, result = create_course_modules(
            user=request.user, 
            course_uuid=course_uuid, 
            data=request.data
        )
        if not success:
            http_status = status.HTTP_404_NOT_FOUND if isinstance(result, dict) and "detail" in result and "Course not found" in result["detail"] else status.HTTP_400_BAD_REQUEST
            return Response(
                {"success": False, "errors": result},
                status=http_status
            )
        return Response(
            {
                "success": True,
                "message": f"Successfully created {len(result)} module(s).",
                "modules": result
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, course_uuid, *args, **kwargs):
        success, queryset_or_error = get_course_modules_queryset(
            user=request.user, 
            course_uuid=course_uuid
        )
        if not success:
            return Response(
                {"success": False, "errors": queryset_or_error},
                status=status.HTTP_404_NOT_FOUND
            )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset_or_error, request, view=self)

        if page is not None:
            serializer = CourseModuleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CourseModuleSerializer(queryset_or_error, many=True)
        return Response(
            {
                "success": True,
                "modules": serializer.data
            },
            status=status.HTTP_200_OK
        )

