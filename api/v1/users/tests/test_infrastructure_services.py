from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from mixer.backend.django import mixer

from api.utils.files import mb_to_bytes
from api.utils.tests import (
    generate_test_image,
    get_expired_email_verification_kwarg,
    is_objects_fields_match,
)
from api.v1.users.constants import EV_CODE_LENGTH, MAX_USER_IMAGE_SIZE_MB
from api.v1.users.models import EmailVerification
from api.v1.users.serializers import (
    CurrentUserSerializer,
    EmailVerificationSerializer,
    UserVerificationSerializer,
)
from api.v1.users.services.infrastructure.user_email_verification import (
    EVSenderService,
    UserEmailVerifierService,
)
from api.v1.users.services.infrastructure.user_update import UserUpdateService

User = get_user_model()


class TestUserUpdateService:
    @pytest.mark.django_db
    def test_update(self, user: User, faker: Faker):
        data = {
            "username": faker.user_name(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "about": faker.text(),
        }
        response = UserUpdateService(
            user,
            CurrentUserSerializer,
            data,
            True,
        ).execute()

        assert response.status_code == HTTPStatus.OK
        assert is_objects_fields_match(
            response.data, user, ("username", "first_name", "last_name", "about")
        )

    @pytest.mark.django_db
    def test_valid_image_size(self, user: User):
        old_image = user.image
        response = UserUpdateService(
            user,
            CurrentUserSerializer,
            {"image": generate_test_image()},
            True,
        ).execute()

        assert response.status_code == HTTPStatus.OK
        assert old_image != user.image

    @pytest.mark.django_db
    def test_invalid_image_size(self, user: User):
        response = UserUpdateService(
            user,
            CurrentUserSerializer,
            {"image": self._image_with_invalid_size},
            True,
        ).execute()

        assert response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        assert not user.image

    @property
    def _image_with_invalid_size(self) -> SimpleUploadedFile:
        image = generate_test_image()
        image.size = mb_to_bytes(MAX_USER_IMAGE_SIZE_MB * 2)
        return image


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_verified, previous_sending, expected_status, error_code",
    [
        (False, False, HTTPStatus.CREATED, None),
        (True, False, HTTPStatus.BAD_REQUEST, "email_already_verified"),
        (False, True, HTTPStatus.TOO_MANY_REQUESTS, "sending_limit_reached"),
    ],
)
def test_ev_sending_service(
    is_verified: bool,
    previous_sending: bool,
    expected_status: int,
    error_code: str | None,
):
    user = mixer.blend("users.User", is_verified=is_verified)
    if previous_sending:
        mixer.blend("users.EmailVerification", user=user)

    service = EVSenderService(
        EmailVerificationSerializer,
        user,
    )
    response = service.execute()

    assert response.status_code == expected_status

    if error_code is not None:
        assert response.data["code"] == error_code

    if expected_status == HTTPStatus.CREATED:
        assert EmailVerification.objects.count() == 1
        email_verification = EmailVerification.objects.first()
        serialized_email_verification = EmailVerificationSerializer(email_verification)
        assert serialized_email_verification.data == response.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_code, expired, expected_status, error_code",
    [
        (False, False, HTTPStatus.OK, None),
        (True, False, HTTPStatus.BAD_REQUEST, "invalid_verification_code"),
        (False, True, HTTPStatus.GONE, "verification_code_expired"),
    ],
)
def test_email_verifier_service(
    unverified_user: User,
    invalid_code: bool,
    expired: bool,
    expected_status: int,
    error_code: str | None,
):
    email_verification = mixer.blend(
        "users.EmailVerification",
        user=unverified_user,
        **get_expired_email_verification_kwarg() if expired else {},
    )

    service = UserEmailVerifierService(
        UserVerificationSerializer,
        CurrentUserSerializer,
        unverified_user,
        {"code": "1" * EV_CODE_LENGTH if invalid_code else email_verification.code},
    )
    response = service.execute()

    assert response.status_code == expected_status
    if expected_status == HTTPStatus.OK:
        assert unverified_user.is_verified
    else:
        assert not unverified_user.is_verified
    if error_code is not None:
        assert response.data["code"] == error_code


if __name__ == "__main__":
    pytest.main()
