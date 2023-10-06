from collections import namedtuple

import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from mixer.backend.django import mixer

from api.utils.tests import get_expired_email_verification_kwarg

User = get_user_model()

EmailChangeData = namedtuple("EmailChangeData", ("user", "password", "new_email"))


@pytest.fixture()
def email_verification():
    return mixer.blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verification():
    return mixer.blend(
        "users.EmailVerification",
        **get_expired_email_verification_kwarg(),
    )


@pytest.fixture()
def email_verifications():
    return mixer.cycle().blend("users.EmailVerification")


@pytest.fixture()
def expired_email_verifications():
    return mixer.cycle().blend(
        "users.EmailVerification",
        **get_expired_email_verification_kwarg(),
    )


@pytest.fixture()
def email_change_test_data(verified_user: User, faker: Faker) -> EmailChangeData:
    new_email = faker.email()
    password = faker.password()

    verified_user.set_password(password)
    verified_user.save()

    return EmailChangeData(
        verified_user,
        password,
        new_email,
    )
