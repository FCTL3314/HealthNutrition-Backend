from http import HTTPStatus

import pytest
from django.urls import reverse

from interactions.models import StoreComment
from stores.models import Store
from utils.static import get_static_file


@pytest.fixture()
def store():
    store = Store.objects.create(
        name='Store',
        url='https://store.com',
        description='Store description',
        logo=get_static_file('images/image_for_tests.jpg'),
    )
    return store


@pytest.fixture()
def comments(user, store):
    return StoreComment.objects.create(author=user, store=store, text='Test comment')


@pytest.mark.django_db
def test_store_detail_view_success(client, store, comments):
    path = reverse('stores:store-detail', args=(store.slug,))

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert response.context_data.get('object') == store
    assert list(response.context_data.get('comments')) == list(store.get_comments())


@pytest.mark.django_db
def test_store_detail_view_404(client, faker):
    fake_slug = faker.slug()
    path = reverse('stores:store-detail', args=(fake_slug,))

    response = client.get(path)

    assert response.status_code == HTTPStatus.NOT_FOUND
