import pytest
from factory import Faker as FactoryFaker
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from faker import Faker

from users.models import User


class TestUserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FactoryFaker('user_name')
    first_name = FactoryFaker('first_name')
    last_name = FactoryFaker('last_name')
    email = FactoryFaker('email')
    password = PostGenerationMethodCall('set_password', Faker().password())


@pytest.fixture()
def user(faker):
    return TestUserFactory()
