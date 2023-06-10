from http import HTTPStatus

import pytest
from django.conf import settings

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
    path = store.get_absolute_url()

    response = client.get(path)

    context_object = response.context_data.get('object')
    context_comments = response.context_data.get('comments')
    context_popular_products = response.context_data.get('popular_products')

    assert response.status_code == HTTPStatus.OK
    assert context_object == store
    assert context_object.views == 1
    assert list(context_comments) == list(store.get_comments())
    assert list(context_popular_products) == list(store.popular_products()[:settings.POPULAR_PRODUCTS_PAGINATE_BY])


if __name__ == '__main__':
    pytest.main()
