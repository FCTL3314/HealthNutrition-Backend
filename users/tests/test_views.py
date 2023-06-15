import pytest
from django.urls import reverse
from http import HTTPStatus
from faker import Faker

from users.forms import RegistrationForm, LoginForm
from users.models import User

faker = Faker()

REMEMBER_ME_AGE = ((60 * 60) * 24) * 14


@pytest.mark.django_db
def test_registration_create_view_get(client):
    response = client.get(reverse("users:registration"))

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.context_data["form"], RegistrationForm)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "expected_status, username, email, password",
    (
            [HTTPStatus.FOUND, faker.user_name(), faker.email(), faker.password()],
            [HTTPStatus.OK, "abc", faker.email(), faker.password()],
            [HTTPStatus.OK, faker.user_name(), "not_email", faker.password()],
            [HTTPStatus.OK, faker.user_name(), faker.email(), "123456"],
    ),
)
def test_registration_create_view_post(client, expected_status, username, email, password):
    data = {
        "username": username,
        "email": email,
        "password1": password,
        "password2": password,
    }

    response = client.post(reverse("users:registration"), data=data)

    assert response.status_code == expected_status
    if response.status_code == HTTPStatus.FOUND:
        assert User.objects.filter(username=username, email=email).exists()


@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse("users:login"))

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.context_data["form"], LoginForm)


@pytest.mark.django_db
@pytest.mark.parametrize("remember_me", (True, False))
def test_login_view_post(client, remember_me):
    password = faker.password()
    user = User.objects.create_user(username=faker.user_name(), email=faker.email(), password=password)

    data = {
        "username": user.username,
        "password": password,
        "remember_me": remember_me,
    }

    response = client.post(reverse("users:login"), data=data)

    assert response.status_code == HTTPStatus.FOUND
    if remember_me:
        assert response.cookies['sessionid']['max-age'] == REMEMBER_ME_AGE
    else:
        assert not response.cookies['sessionid']['max-age']


if __name__ == "__main__":
    pytest.main()
