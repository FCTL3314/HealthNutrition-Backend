import pytest
from cacheops import invalidate_all
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.base.time_providers import UTCTimeProvider
from api.v1.categories.constants import CATEGORIES_PAGINATE_BY
from api.v1.categories.models import Category
from api.v1.nutrition.models import Nutrition
from api.v1.products.models import Product

User = get_user_model()


@pytest.fixture()
def user() -> User:
    return mixer.blend("users.User")


@pytest.fixture()
def admin_user(user: User) -> User:
    user.is_staff = True
    user.is_superuser = True
    user.save(update_fields=("is_staff", "is_superuser"))
    return user


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
def category() -> Category:
    return mixer.blend("categories.Category")


@pytest.fixture()
def categories() -> list[Category]:
    return mixer.cycle(CATEGORIES_PAGINATE_BY * 2).blend("categories.Category")


@pytest.fixture()
def product() -> Product:
    return mixer.blend("products.Product")


@pytest.fixture()
def products() -> list[Product]:
    return mixer.cycle(5).blend("products.Product")


@pytest.fixture()
def nutrition() -> Nutrition:
    return mixer.blend("nutrition.Nutrition")


@pytest.fixture()
def utc_time_provider() -> UTCTimeProvider:
    return UTCTimeProvider()


@pytest.fixture(autouse=True)
def clear_test_cache() -> None:
    """
    Deletes the entire cache created by the test.
    """
    invalidate_all()
