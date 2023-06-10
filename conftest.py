import pytest

from users.tests import UserTestFactory


@pytest.fixture()
def user(faker):
    return UserTestFactory()
