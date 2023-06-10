from factory import Faker
from factory.django import DjangoModelFactory

from stores.models import Store


class StoreTestFactory(DjangoModelFactory):
    class Meta:
        model = Store
        django_get_or_create = ('name',)

    name = Faker('company')
    url = Faker('url')
    description = Faker('text')
    logo = Faker('file_path', extension='jpg')
