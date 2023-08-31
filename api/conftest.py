import pytest
from mixer.backend.django import mixer

from api.common.time_providers import UTCTimeProvider


@pytest.fixture()
def user():
    return mixer.blend("users.User")


@pytest.fixture()
def verified_user():
    return mixer.blend("users.User", is_verified=True)


@pytest.fixture()
def unverified_user():
    return mixer.blend("users.User", is_verified=False)


@pytest.fixture()
def users():
    return mixer.cycle(5).blend("users.User")


@pytest.fixture()
def store():
    return mixer.blend("stores.Store")


@pytest.fixture()
def product_type():
    return mixer.blend("products.ProductType")


@pytest.fixture()
def product():
    return mixer.blend("products.Product")


@pytest.fixture()
def utc_time_provider():
    return UTCTimeProvider()
