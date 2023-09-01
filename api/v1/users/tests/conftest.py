import pytest
from mixer.backend.django import mixer

from api.utils.tests import get_expired_email_verification_kwargs


@pytest.fixture()
def email_verification():
    return mixer.blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verification():
    return mixer.blend(
        "users.EmailVerification",
        **get_expired_email_verification_kwargs(),
    )


@pytest.fixture()
def email_verifications():
    return mixer.cycle().blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verifications():
    return mixer.cycle().blend(
        "users.EmailVerification",
        **get_expired_email_verification_kwargs(),
    )
