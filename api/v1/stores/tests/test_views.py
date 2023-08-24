from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.reverse import reverse

from api.utils.tests import generate_test_image, get_authorization_header
from api.v1.stores.constants import STORES_PAGINATE_BY
from api.v1.stores.models import Store

User = get_user_model()


STORE_DETAIL = "api:v1:stores:stores-detail"
STORE_LIST = "api:v1:stores:stores-list"


@pytest.mark.django_db
def test_store_detail(client, store: Store):
    path = reverse(STORE_DETAIL, args=(store.slug,))

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert response.data.get("id") == store.id


@pytest.mark.django_db
def test_store_list(client, stores: list[Store]):
    path = reverse(STORE_LIST)

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert len(response.data.get("results")) == STORES_PAGINATE_BY


@pytest.mark.django_db
def test_store_update(client, store: Store, admin_user: User, faker: Faker):
    path = reverse(STORE_DETAIL, args=(store.slug,))

    data = {
        "name": faker.name(),
    }

    response = client.patch(
        path,
        data=data,
        content_type="application/json",
        **get_authorization_header(admin_user),
    )

    store.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert store.name == data["name"]


@pytest.mark.django_db
def test_store_create(client, admin_user: User, faker: Faker):
    path = reverse(STORE_LIST)

    data = {
        "name": faker.name(),
        "url": faker.url(),
        "logo": generate_test_image(),
        "description": faker.text(),
    }

    assert Store.objects.count() == 0

    response = client.post(
        path,
        data=data,
        **get_authorization_header(admin_user),
    )

    assert response.status_code == HTTPStatus.CREATED
    assert Store.objects.count() == 1


@pytest.mark.django_db
def test_store_destroy(client, store: Store, admin_user: User):
    path = reverse(STORE_DETAIL, args=(store.slug,))

    assert Store.objects.count() == 1

    response = client.delete(
        path,
        **get_authorization_header(admin_user),
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert Store.objects.count() == 0


if __name__ == "__main__":
    pytest.main()
