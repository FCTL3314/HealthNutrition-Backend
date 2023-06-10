from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from products.models import Product, ProductType
from stores.tests import StoreTestFactory


class ProductTypeTestFactory(DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ('name',)

    name = Faker('word')
    description = Faker('text')
    image = Faker('file_path', extension='jpg')


class ProductTestFactory(DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('name',)

    name = Faker('word')
    price = Faker('pyfloat', min_value=1.0, max_value=1000.0, right_digits=2)
    card_description = Faker('text')
    description = Faker('text')
    image = Faker('file_path', extension='jpg')
    created_at = Faker('date_time')
    updated_at = Faker('date_time')
    store = SubFactory(StoreTestFactory)
    product_type = SubFactory(ProductTypeTestFactory)
