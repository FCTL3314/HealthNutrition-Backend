import random
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer

from api.utils.tests import get_auth_header
from api.v1.users.models import EmailVerification

User = get_user_model()


class TestEmailVerificationCreateView:
    URL_PATTERN = "api:v1:users:verification-send"
    path = reverse(URL_PATTERN)

    @pytest.mark.django_db
    def test_success(self, client, user: User):
        response = client.post(self.path, **get_auth_header(user))

        assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.django_db
    def test_sending_limit_reached(self, client, user: User):
        mixer.blend("users.EmailVerification", user=user)
        response = client.post(self.path, **get_auth_header(user))

        assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
        assert "retry_after" in response.data["messages"]

    @pytest.mark.django_db
    def test_already_verified(self, client, verified_user: User):
        response = client.post(self.path, **get_auth_header(verified_user))

        assert response.status_code == HTTPStatus.BAD_REQUEST


class TestUserVerifyUpdateView:
    URL_PATTERN = "api:v1:users:verify"
    path = reverse(URL_PATTERN)

    @pytest.mark.django_db
    def test_success(self, client, email_verification: EmailVerification):
        response = client.patch(
            self.path,
            data={"code": email_verification.code},
            content_type="application/json",
            **get_auth_header(email_verification.user),
        )

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.django_db
    def test_invalid_verification_code(
        self, client, email_verification: EmailVerification
    ):
        response = client.patch(
            self.path,
            data={"code": self._create_invalid_code(email_verification.code)},
            content_type="application/json",
            **get_auth_header(email_verification.user),
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.django_db
    def test_verification_expired(
        self, client, expired_email_verification: EmailVerification
    ):
        response = client.patch(
            self.path,
            data={"code": expired_email_verification.code},
            content_type="application/json",
            **get_auth_header(expired_email_verification.user),
        )

        assert response.status_code == HTTPStatus.GONE

    @staticmethod
    def _create_invalid_code(code: str) -> str:
        initial_code = list(code)
        invalid_code = list(code)
        while invalid_code == initial_code:
            random.shuffle(invalid_code)
        return "".join(invalid_code)


if __name__ == "__main__":
    pytest.main()