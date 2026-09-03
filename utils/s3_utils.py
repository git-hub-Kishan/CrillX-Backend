from django.conf import settings


def get_file_url(file_key_or_url):
    """
    Returns the resolved URL for a given file key or stored URL.
    If settings.USE_S3_TOGGLE is enabled, attempts to generate and return a presigned download URL.
    Otherwise, returns whatever is stored in the database field directly.
    """
    if not file_key_or_url:
        return None

    if getattr(settings, 'USE_S3_TOGGLE', False):
        try:
            from users.services.s3_services import generate_presigned_download_url
            success, result = generate_presigned_download_url(file_key_or_url)
            if success:
                return result
        except Exception:
            pass

    return file_key_or_url
