import pytest
from django.urls import reverse
from http import HTTPStatus
from faker import Faker

from users.forms import RegistrationForm
from users.models import User

faker = Faker()


@pytest.mark.django_db
def test_registration_create_view_get(client):
    path = reverse("users:registration")

    response = client.get(path)

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
    path = reverse("users:registration")

    data = {
        "username": username,
        "email": email,
        "password1": password,
        "password2": password,
    }

    response = client.post(path, data=data)

    assert response.status_code == expected_status
    if response.status_code == HTTPStatus.FOUND:
        assert User.objects.filter(username=username, email=email).exists()


if __name__ == "__main__":
    pytest.main()
