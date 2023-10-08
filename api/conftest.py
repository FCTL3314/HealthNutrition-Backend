import pytest
from cacheops import invalidate_all
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.base.time_providers import UTCTimeProvider
from api.v1.products.models import ProductType, Product
from api.v1.stores.models import Store

User = get_user_model()


@pytest.fixture()
def user() -> User:
    return mixer.blend("users.User")


@pytest.fixture()
def verified_user() -> User:
    return mixer.blend("users.User", is_verified=True)


@pytest.fixture()
def unverified_user() -> User:
    return mixer.blend("users.User", is_verified=False)


@pytest.fixture()
def users() -> list[User]:
    return mixer.cycle().blend("users.User")


@pytest.fixture()
def store() -> Store:
    return mixer.blend("stores.Store")


@pytest.fixture()
def product_type() -> ProductType:
    return mixer.blend("products.ProductType")


@pytest.fixture()
def product() -> Product:
    return mixer.blend("products.Product")


@pytest.fixture()
def utc_time_provider() -> UTCTimeProvider:
    return UTCTimeProvider()


@pytest.fixture(autouse=True)
def clear_test_cache() -> None:
    """
    Deletes the entire cache created by the test.
    """
    invalidate_all()
