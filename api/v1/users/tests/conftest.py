from datetime import timedelta

import pytest
from django.utils.timezone import now
from mixer.backend.django import mixer

from api.v1.users.constants import EV_EXPIRATION


@pytest.fixture()
def email_verification():
    return mixer.blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verification():
    return mixer.blend(
        "users.EmailVerification",
        expiration=now() - timedelta(seconds=EV_EXPIRATION),
    )


@pytest.fixture()
def email_verifications():
    return mixer.cycle(5).blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verifications():
    return mixer.cycle(5).blend(
        "users.EmailVerification",
        expiration=now() - timedelta(seconds=EV_EXPIRATION),
    )
