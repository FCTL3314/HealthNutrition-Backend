import pytest
from cacheops import invalidate_all
from mixer.backend.django import mixer

from api.base.time_providers import UTCTimeProvider


@pytest.fixture()
def user():
    user = mixer.blend("users.User")
    yield user
    user.delete()


@pytest.fixture()
def verified_user():
    user = mixer.blend("users.User", is_verified=True)
    yield user
    user.delete()


@pytest.fixture()
def unverified_user():
    user = mixer.blend("users.User", is_verified=False)
    yield user
    user.delete()


@pytest.fixture()
def users():
    users = mixer.cycle().blend("users.User")
    yield users
    users.delete()


@pytest.fixture()
def store():
    store = mixer.blend("stores.Store")
    yield store
    store.delete()


@pytest.fixture()
def product_type():
    product_type = mixer.blend("products.ProductType")
    yield product_type
    product_type.delete()


@pytest.fixture()
def product():
    product = mixer.blend("products.Product")
    yield product
    product.delete()


@pytest.fixture()
def utc_time_provider():
    return UTCTimeProvider()


@pytest.fixture(autouse=True)
def clear_test_cache():
    invalidate_all()
