from api.utils.files import bytes_to_mb
from api.v1.users.constants import MAX_USER_IMAGE_SIZE_MB


def is_user_image_size_valid(bytes_size: int) -> bool:
    """
    Determines whether the user's image has a valid size.
    """
    image_size_mb = bytes_to_mb(bytes_size)
    return image_size_mb <= MAX_USER_IMAGE_SIZE_MB
