from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.v1.users.models import EmailVerification
from api.v1.users.serializers import EmailVerificationSerializer
from api.v1.users.services.email_verification import EVSenderService

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_verified, previous_sending, expected_status",
    [
        (False, False, HTTPStatus.CREATED),
        (True, False, HTTPStatus.BAD_REQUEST),
        (False, True, HTTPStatus.TOO_MANY_REQUESTS),
    ],
)
def test_ev_sending_service(
    is_verified: bool, previous_sending: bool, expected_status: int
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

    if expected_status == HTTPStatus.CREATED:
        assert EmailVerification.objects.count() == 1


if __name__ == "__main__":
    pytest.main()
