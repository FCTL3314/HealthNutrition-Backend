import pytest
from django.utils.timezone import now
from mixer.backend.django import mixer

from api.v1.users.constants import EV_EXPIRATION_TIMEDELTA


@pytest.fixture()
def email_verification():
    return mixer.blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verification():
    return mixer.blend(
        "users.EmailVerification",
        expiration=now() - EV_EXPIRATION_TIMEDELTA,
    )


@pytest.fixture()
def email_verifications():
    return mixer.cycle().blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verifications():
    return mixer.cycle().blend(
        "users.EmailVerification",
        expiration=now() - EV_EXPIRATION_TIMEDELTA,
    )
