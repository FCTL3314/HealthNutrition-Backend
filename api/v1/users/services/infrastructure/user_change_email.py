from http import HTTPStatus
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from api.base.services import IService
from api.responses import APIResponse
from api.utils.errors import Error
from api.v1.users.serializers import CurrentUserSerializer

User = get_user_model()


class ChangeEmailErrors:
    INVALID_PASSWORD = Error("The password entered is incorrect.", "invalid_password")
    SAME_EMAIL = Error("The new email is the same as the old one.", "same_email")


class UserChangeEmailService(IService):
    """
    Changes the user's e-mail address by requesting
    a new e-mail address and their password.
    """

    def __init__(
        self, serializer_class: type[Serializer], user: User, data: dict[str, Any]
    ):
        self._serializer = serializer_class(data=data)
        self._serializer.is_valid(raise_exception=True)
        self.__new_email = self._serializer.validated_data["new_email"]
        self.__password = self._serializer.validated_data["password"]
        self._user = user

    def execute(self) -> APIResponse:
        if not self._user.check_password(self.__password):
            return self._password_is_incorrect_response()
        if self._user.email == self.__new_email:
            return self._same_email_response()
        self._user.update_email(self.__new_email)
        self._user.make_unverified()
        return self._email_successfully_changed_response()

    @staticmethod
    def _password_is_incorrect_response() -> APIResponse:
        return APIResponse(
            detail=ChangeEmailErrors.INVALID_PASSWORD.message,
            code=ChangeEmailErrors.INVALID_PASSWORD.code,
            status=HTTPStatus.BAD_REQUEST,
        )

    @staticmethod
    def _same_email_response() -> APIResponse:
        return APIResponse(
            detail=ChangeEmailErrors.SAME_EMAIL.message,
            code=ChangeEmailErrors.SAME_EMAIL.code,
            status=HTTPStatus.BAD_REQUEST,
        )

    def _email_successfully_changed_response(self) -> APIResponse:
        return APIResponse(
            CurrentUserSerializer(self._user).data,
            status=HTTPStatus.OK,
        )
