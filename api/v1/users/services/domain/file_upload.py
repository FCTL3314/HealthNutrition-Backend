from api.utils.files import bytes_to_mb
from api.v1.users.constants import MAX_IMAGE_UPLOAD_SIZE_MB


def is_image_size_valid(bytes_size: int) -> bool:
    """
    Determines whether the image has a valid size.
    """
    image_size_mb = bytes_to_mb(bytes_size)
    return image_size_mb <= MAX_IMAGE_UPLOAD_SIZE_MB
