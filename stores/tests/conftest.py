import pytest
from django.conf import settings
from mixer.backend.django import mixer


@pytest.fixture()
def store():
    return mixer.blend("stores.Store")


@pytest.fixture()
def stores():
    return mixer.cycle(settings.STORES_PAGINATE_BY * 2).blend("stores.Store")
