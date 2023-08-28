import pytest
from mixer.backend.django import mixer

from api.v1.stores.constants import STORES_PAGINATE_BY


@pytest.fixture()
def stores():
    return mixer.cycle(STORES_PAGINATE_BY * 2).blend("stores.Store")
