from http import HTTPStatus

import pytest
from django.urls import reverse

from interactions.models import StoreComment
from stores.tests import TestStoreFactory


@pytest.fixture()
def store(faker):
    return TestStoreFactory()


@pytest.fixture()
def comments(user, store, faker):
    return StoreComment.objects.create(author=user, store=store, text=faker.text())


@pytest.mark.django_db
def test_store_detail_view_success(client, store, comments):
    path = reverse('stores:store-detail', args=(store.slug,))

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert response.context_data.get('object') == store
    assert list(response.context_data.get('comments')) == list(store.get_comments())


@pytest.mark.django_db
def test_store_detail_view_404(client, faker):
    path = reverse('stores:store-detail', args=(faker.slug(),))

    response = client.get(path)

    assert response.status_code == HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    pytest.main()
