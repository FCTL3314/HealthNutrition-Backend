import random
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from mixer.backend.django import mixer

from api.utils.tests import get_auth_header
from api.v1.users.models import EmailVerification
from api.v1.users.tests.conftest import EmailChangeData

User = get_user_model()


class TestUserChangeEmailView:
    URL_PATTERN = "api:v1:users:change-email"
    path = reverse(URL_PATTERN)

    @pytest.mark.django_db
    def test_success(self, client, email_change_test_data: EmailChangeData):
        response = client.post(
            self.path,
            data={
                "new_email": email_change_test_data.new_email,
                "password": email_change_test_data.password,
            },
            **get_auth_header(email_change_test_data.user),
        )

        assert response.status_code == HTTPStatus.OK
        assert response.data["email"] == email_change_test_data.new_email
        assert response.data["is_verified"] is False

    @pytest.mark.django_db
    def test_same_email(self, client, email_change_test_data: EmailChangeData):
        data = {
            "new_email": email_change_test_data.user.email,
            "password": email_change_test_data.password,
        }
        response = client.post(
            self.path, data=data, **get_auth_header(email_change_test_data.user)
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data["code"] == "same_email"

    @pytest.mark.django_db
    def test_invalid_password(
        self, client, email_change_test_data: EmailChangeData, faker: Faker
    ):
        data = {
            "new_email": email_change_test_data.user.email,
            "password": faker.password(),
        }
        response = client.post(
            self.path, data=data, **get_auth_header(email_change_test_data.user)
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.data["code"] == "invalid_password"


class TestUserSendEmailVerificationView:
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
        assert len(response.data["messages"]) == 1

    @pytest.mark.django_db
    def test_already_verified(self, client, verified_user: User):
        response = client.post(self.path, **get_auth_header(verified_user))

        assert response.status_code == HTTPStatus.BAD_REQUEST


class TestUserEmailVerifierView:
    URL_PATTERN = "api:v1:users:verify"
    path = reverse(URL_PATTERN)

    @pytest.mark.django_db
    def test_success(self, client, email_verification: EmailVerification):
        response = client.post(
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
        response = client.post(
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
        response = client.post(
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
