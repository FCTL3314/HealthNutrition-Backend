import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def user(faker):
    return mixer.blend('users.User')
