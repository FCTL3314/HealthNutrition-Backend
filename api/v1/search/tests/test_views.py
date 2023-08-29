from http import HTTPStatus

import pytest
from django.db.models import Model
from django.urls import reverse
from mixer.backend.django import mixer

from api.v1.products.models import Product, ProductType

PRODUCT_TYPE_SEARCH = "api:v1:search:product-type"
PRODUCT_SEARCH = "api:v1:search:product"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path, model, search_field",
    [
        (reverse(PRODUCT_TYPE_SEARCH), ProductType, "name"),
        (reverse(PRODUCT_TYPE_SEARCH), ProductType, "description"),
        (reverse(PRODUCT_SEARCH), Product, "name"),
        (reverse(PRODUCT_SEARCH), Product, "card_description"),
    ],
)
def test_search_list_view(client, path: str, model: type[Model], search_field: str):
    model_object = mixer.blend(model)

    response = client.get(
        path,
        data={"query": getattr(model_object, search_field)},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data["count"] > 0


if __name__ == "__main__":
    pytest.main()
