from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.helpers.s3_helpers import ALLOWED_S3_FOLDERS
from users.services.s3_services import generate_presigned_upload_url


class S3PresignedUrlAPIView(APIView):
    """
    API View to generate a secure presigned upload URL for S3.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        folder_name = request.data.get('folder')
        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')

        # Basic Validation
        if not all([folder_name, file_name, file_type]):
            return Response(
                {
                    "success": False,
                    "error": "Missing required fields: 'folder', 'file_name', or 'file_type'."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Folder Validation against allowed folders
        if folder_name not in ALLOWED_S3_FOLDERS:
            return Response(
                {
                    "success": False,
                    "error": f"Invalid folder. Allowed folders are: {', '.join(ALLOWED_S3_FOLDERS)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate the presigned URL
        success, result = generate_presigned_upload_url(folder_name, file_name, file_type)

        if not success:
            return Response(
                {
                    "success": False,
                    "error": result
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "success": True,
                "upload_url": result["upload_url"],
                "file_key": result["file_key"]
            },
            status=status.HTTP_200_OK
        )
