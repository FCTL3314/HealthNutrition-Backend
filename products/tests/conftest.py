import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def product():
    return mixer.blend('products.Product')


@pytest.fixture()
def products():
    return mixer.cycle(5).blend('products.Product')
