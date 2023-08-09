import pytest
from mixer.backend.django import mixer

from api.v1.products.constants import PRODUCT_TYPES_PAGINATE_BY


@pytest.fixture()
def product_type():
    return mixer.blend("products.ProductType")


@pytest.fixture()
def product_types():
    return mixer.cycle(PRODUCT_TYPES_PAGINATE_BY * 2).blend("products.ProductType")


@pytest.fixture()
def product():
    return mixer.blend("products.Product")


@pytest.fixture()
def products():
    return mixer.cycle(5).blend("products.Product")
