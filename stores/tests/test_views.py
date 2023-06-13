from http import HTTPStatus

import pytest
from django.conf import settings
from mixer.backend.django import mixer

from common.tests import common_detail_view_tests


@pytest.fixture()
def store():
    return mixer.blend('stores.Store')


@pytest.mark.django_db
def test_store_detail_view(client, store):
    comments = mixer.cycle(settings.COMMENTS_PAGINATE_BY * 2).blend('interactions.StoreComment', store=store)

    path = store.get_absolute_url()

    response = client.get(path)
    context_popular_products = response.context_data['popular_products']

    assert response.status_code == HTTPStatus.OK
    assert len(context_popular_products) == len(store.popular_products()[:settings.PRODUCTS_PAGINATE_BY])
    common_detail_view_tests(response, store, comments)


if __name__ == '__main__':
    pytest.main()
