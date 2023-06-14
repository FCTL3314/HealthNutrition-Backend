import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def store():
    return mixer.blend("stores.Store")
