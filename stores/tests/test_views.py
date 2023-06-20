from http import HTTPStatus

import pytest
from django.conf import settings
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_store_detail_view(client, store):
    products = mixer.cycle(5).blend("products.Product", store=store)

    path = store.get_absolute_url()

    response = client.get(path)

    context_popular_products = response.context_data["popular_products"]

    assert response.status_code == HTTPStatus.OK
    assert len(context_popular_products) == len(products[: settings.PRODUCTS_PAGINATE_BY])


if __name__ == "__main__":
    pytest.main()
