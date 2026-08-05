import logging
import uuid
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)

def get_s3_client():
    """Returns a boto3 S3 client initialized with Django settings."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

def generate_presigned_upload_url(folder_name, file_name, file_type, expiration=3600):
    """
    Generate a presigned URL to upload a file to S3 using PUT.
    Returns a dictionary containing the URL and the file_key.
    """
    s3_client = get_s3_client()
    
    # Generate a unique filename to prevent overwrites
    unique_file_name = f"{uuid.uuid4().hex}_{file_name}"
    object_name = f"{folder_name}/{unique_file_name}"

    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': object_name,
                'ContentType': file_type
            },
            ExpiresIn=expiration
        )
        return True, {
            'upload_url': url,
            'file_key': object_name
        }
    except ClientError as e:
        logger.error(f"Error generating presigned PUT URL: {e}")
        return False, "Could not generate upload URL"
    except Exception as e:
        logger.error(f"Unexpected error generating presigned PUT URL: {e}")
        return False, "An unexpected error occurred"


def generate_presigned_download_url(file_key, expiration=3600):
    """
    Generate a presigned URL to download a file from S3 securely.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=expiration
        )
        return True, response
    except ClientError as e:
        logger.error(f"Error generating presigned GET URL: {e}")
        return False, "Could not generate download URL"


def delete_file_from_s3(file_key):
    """
    Delete a specific file from the S3 bucket.
    """
    s3_client = get_s3_client()
    try:
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=file_key
        )
        return True, "File deleted successfully"
    except ClientError as e:
        logger.error(f"Error deleting file from S3: {e}")
        return False, "Could not delete file"
