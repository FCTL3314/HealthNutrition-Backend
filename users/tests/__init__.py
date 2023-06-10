from factory import Faker as FactoryFaker
from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from faker import Faker

from users.models import User


class UserTestFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = FactoryFaker('user_name')
    first_name = FactoryFaker('first_name')
    last_name = FactoryFaker('last_name')
    email = FactoryFaker('email')
    password = PostGenerationMethodCall('set_password', Faker().password())
