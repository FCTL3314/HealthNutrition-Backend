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
    EMAIL_ALREADY_IN_USE = Error(
        "The email is already in use by another user.", "email_already_in_use"
    )


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
        if self._is_new_email_same_as_old():
            return self._same_email_response()
        if self._is_email_in_use():
            return self._email_already_in_use_response()

        self._user.update_email(self.__new_email)
        self._user.make_unverified()

        return self._email_successfully_changed_response()

    def _is_new_email_same_as_old(self):
        """
        Checks whether the new email is the same as
        the old one.
        """
        return self._user.email == self.__new_email

    def _is_email_in_use(self):
        """
        Checks whether the new email is used by other user.
        """
        return User.objects.filter(email=self.__new_email).exists()

    def _email_successfully_changed_response(self) -> APIResponse:
        return APIResponse(
            CurrentUserSerializer(self._user).data,
            status=HTTPStatus.OK,
        )

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

    @staticmethod
    def _email_already_in_use_response() -> APIResponse:
        return APIResponse(
            detail=ChangeEmailErrors.EMAIL_ALREADY_IN_USE.message,
            code=ChangeEmailErrors.EMAIL_ALREADY_IN_USE.code,
            status=HTTPStatus.BAD_REQUEST,
        )
