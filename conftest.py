import pytest
from django.conf import settings
from mixer.backend.django import mixer


@pytest.fixture()
def user(faker):
    return mixer.blend('users.User')


@pytest.fixture()
def product_type():
    return mixer.blend('products.ProductType')


@pytest.fixture()
def product_types():
    return mixer.cycle(settings.PRODUCT_TYPES_PAGINATE_BY * 2).blend('products.ProductType')
