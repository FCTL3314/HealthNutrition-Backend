from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from api.common.services import AbstractService
from api.responses import APIResponse

User = get_user_model()


class ProductCommentAddService(AbstractService):
    def __init__(
        self,
        serializer_class: type[Serializer],
        user: User,
        data: dict,
    ):
        self._serializer = serializer_class(data=data)
        self._serializer.is_valid(raise_exception=True)
        self._user = user
        self._data = data

    def execute(self) -> APIResponse:
        self._serializer.save(author=self._user)
        return APIResponse(self._serializer.data, status=HTTPStatus.CREATED)
