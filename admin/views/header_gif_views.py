from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import StandardResultsSetPagination
from utils.permissions import IsSuperAdminUser
from admin.serializers.header_gif_serializers import (
    HeaderGIFListSerializer,
    HeaderGIFDetailSerializer,
    HeaderGIFCreateUpdateSerializer,
    ActiveHeaderGIFResponseSerializer,
)
from admin.services.header_gif_services import (
    get_header_gifs_queryset,
    get_header_gif_by_identifier,
    create_header_gif,
    update_header_gif,
    delete_header_gif,
    get_active_header_gif_for_client,
)


class AdminHeaderGIFListCreateAPIView(APIView):
    """
    Admin API endpoint to list all header GIFs with search/filters/pagination or create a new GIF banner.
    GET  /admin/header-gifs/
    POST /admin/header-gifs/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search')
        status_query = request.query_params.get('status')
        audience_query = request.query_params.get('target_audience')

        queryset = get_header_gifs_queryset(
            search=search_query,
            status=status_query,
            target_audience=audience_query,
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = HeaderGIFListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = HeaderGIFListSerializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "count": queryset.count(),
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = HeaderGIFCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = create_header_gif(serializer.validated_data)
        detail_serializer = HeaderGIFDetailSerializer(instance)

        return Response(
            {
                "success": True,
                "message": "Header GIF banner created and scheduled successfully.",
                "banner": detail_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class AdminHeaderGIFDetailAPIView(APIView):
    """
    Admin API endpoint to retrieve, partially update, or delete a specific header GIF banner.
    GET    /admin/header-gifs/<identifier>/
    PATCH  /admin/header-gifs/<identifier>/
    DELETE /admin/header-gifs/<identifier>/
    """
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, identifier, *args, **kwargs):
        instance = get_header_gif_by_identifier(identifier)
        if not instance:
            return Response(
                {
                    "success": False,
                    "message": "Header GIF banner not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = HeaderGIFDetailSerializer(instance)
        return Response(
            {
                "success": True,
                "banner": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, identifier, *args, **kwargs):
        instance = get_header_gif_by_identifier(identifier)
        if not instance:
            return Response(
                {
                    "success": False,
                    "message": "Header GIF banner not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = HeaderGIFCreateUpdateSerializer(
            instance,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_instance = update_header_gif(instance, serializer.validated_data)
        detail_serializer = HeaderGIFDetailSerializer(updated_instance)

        return Response(
            {
                "success": True,
                "message": "Header GIF banner updated successfully.",
                "banner": detail_serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, identifier, *args, **kwargs):
        instance = get_header_gif_by_identifier(identifier)
        if not instance:
            return Response(
                {
                    "success": False,
                    "message": "Header GIF banner not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        success, message = delete_header_gif(instance)
        if not success:
            return Response(
                {
                    "success": False,
                    "message": message
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


class ActiveHeaderGIFAPIView(APIView):
    """
    Public / Client API endpoint to fetch the currently active Header GIF banner.
    GET /users/header-gif/active/
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        audience = request.query_params.get('audience')
        active_banner = get_active_header_gif_for_client(
            audience=audience,
            user=request.user if request.user.is_authenticated else None
        )

        if not active_banner:
            return Response(
                {
                    "success": True,
                    "has_active_gif": False,
                    "active_gif": None
                },
                status=status.HTTP_200_OK
            )

        serializer = ActiveHeaderGIFResponseSerializer(active_banner)
        return Response(
            {
                "success": True,
                "has_active_gif": True,
                "active_gif": serializer.data
            },
            status=status.HTTP_200_OK
        )
