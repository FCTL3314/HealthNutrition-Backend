import pytest
from factory import Faker
from factory.django import DjangoModelFactory

from users.models import User


class TestUserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = Faker('password')


@pytest.fixture()
def user(faker):
    return TestUserFactory()
