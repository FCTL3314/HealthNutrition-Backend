from http import HTTPStatus

from django.core.files.uploadedfile import TemporaryUploadedFile

from api.base.services import ServiceProto
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.v1.users.constants import MAX_USER_IMAGE_SIZE_MB
from api.v1.users.services.domain.file_upload import is_user_image_size_valid


class UserImageUploadErrors:
    IMAGE_SIZE_TOO_LARGE = ErrorMessage(
        (
            f"The size of the loaded image must be less than "
            f"or equal to {MAX_USER_IMAGE_SIZE_MB} mb."
        ),
        "image_size_too_large",
    )


class UserImageUploadService(ServiceProto):
    """
    Verifies that the image uploaded by the user is correct.
    """

    def __init__(self, image: TemporaryUploadedFile | None):
        self._image = image

    def execute(self) -> APIResponse | None:
        if self._image is None:
            return
        if not is_user_image_size_valid(self._image.size):
            return self.image_size_too_large_response()

    @staticmethod
    def image_size_too_large_response() -> APIResponse:
        return APIResponse(
            detail=UserImageUploadErrors.IMAGE_SIZE_TOO_LARGE.message,
            code=UserImageUploadErrors.IMAGE_SIZE_TOO_LARGE.code,
            status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        )
