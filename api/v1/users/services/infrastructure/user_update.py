from http import HTTPStatus

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework.response import Response

from api.base.services import ServiceProto
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.v1.users.constants import MAX_USER_IMAGE_SIZE_MB
from api.v1.users.services.domain.file_upload import is_user_image_size_valid


class UserUpdateErrors:
    IMAGE_SIZE_TOO_LARGE = ErrorMessage(
        (
            f"The size of the loaded image must be less than "
            f"or equal to {MAX_USER_IMAGE_SIZE_MB} mb."
        ),
        "image_size_too_large",
    )


class UserUpdateService(ServiceProto):
    """
    Updates the user by calling the standard method of
    updating the model object in django if the conditions
    are met.
    """

    def __init__(
        self,
        image: TemporaryUploadedFile | None,
        default_update_callback: callable,
    ):
        self._image = image
        self._default_update_callback = default_update_callback

    def execute(self) -> APIResponse | Response:
        if self._image is not None and not is_user_image_size_valid(self._image.size):
            return self.invalid_image_size_response()
        return self._default_update_callback()

    @staticmethod
    def invalid_image_size_response() -> APIResponse:
        return APIResponse(
            detail=UserUpdateErrors.IMAGE_SIZE_TOO_LARGE.message,
            code=UserUpdateErrors.IMAGE_SIZE_TOO_LARGE.code,
            status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        )
