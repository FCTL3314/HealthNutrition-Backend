from http import HTTPStatus
from typing import Any

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Model
from rest_framework.serializers import Serializer

from api.base.services import ServiceProto
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.utils.models import invalidate_prefetch_cache
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
    Responsible for updating the user object, validates
    conditions such as:
        The size of the uploaded image.
    """

    def __init__(
        self,
        instance: Model,
        serializer_class: type[Serializer],
        data: dict[str, Any],
        partial: bool,
    ):
        self._instance = instance
        self._serializer = serializer_class(self._instance, data=data, partial=partial)
        self._serializer.is_valid(raise_exception=True)
        self._data = data
        self._image: TemporaryUploadedFile = data.get("image")

    def execute(self) -> APIResponse:
        if self._image is not None and not is_user_image_size_valid(self._image.size):
            return self.invalid_image_size_response()
        self._serializer.save()
        invalidate_prefetch_cache(self._instance)
        return self._successfully_updated_response()

    def _successfully_updated_response(self) -> APIResponse:
        return APIResponse(self._serializer.data)

    @staticmethod
    def invalid_image_size_response() -> APIResponse:
        return APIResponse(
            detail=UserUpdateErrors.IMAGE_SIZE_TOO_LARGE.message,
            code=UserUpdateErrors.IMAGE_SIZE_TOO_LARGE.code,
            status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        )
