from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from interactions.models import ProductComment, StoreComment
from products.tests import ProductTestFactory
from stores.tests import StoreTestFactory
from users.tests import UserTestFactory


class ProductCommentTestFactory(DjangoModelFactory):
    class Meta:
        model = ProductComment

    author = SubFactory(UserTestFactory)
    product = SubFactory(ProductTestFactory)
    text = Faker('text')
    created_at = Faker('date_time')


class StoreCommentTestFactory(DjangoModelFactory):
    class Meta:
        model = StoreComment

    author = SubFactory(UserTestFactory)
    store = SubFactory(StoreTestFactory)
    text = Faker('text')
    created_at = Faker('date_time')
