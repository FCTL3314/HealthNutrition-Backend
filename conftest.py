import pytest
from faker import Faker

from users.models import User


@pytest.fixture()
def user():
    user = User.objects.create(
        username='TestUser',
        first_name='Test',
        last_name='User',
        email='email@example.com',
        password='qnjCmk27yzKTCWWiwdYH',
    )
    return user


@pytest.fixture()
def faker():
    return Faker()
