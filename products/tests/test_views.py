from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from django.conf import settings
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_product_type_list_view(client, product_types):
    path = reverse("products:product-types")

    response = client.get(path)

    context_object_list = response.context_data.get("object_list")

    assert response.status_code == HTTPStatus.OK
    assert len(context_object_list) == len(
        product_types[: settings.PRODUCT_TYPES_PAGINATE_BY]
    )


@pytest.mark.django_db
def test_product_list_view(client, product_type):
    products = mixer.cycle(settings.PRODUCTS_PAGINATE_BY * 2).blend(
        "products.Product", product_type=product_type
    )

    path = reverse("products:products", args=(product_type.slug,))

    response = client.get(path)

    product_type.refresh_from_db()
    context_object_list = response.context_data.get("object_list")

    assert response.status_code == HTTPStatus.OK
    assert product_type.views == 1
    assert len(context_object_list) == len(products[: settings.PRODUCTS_PAGINATE_BY])


@pytest.mark.django_db
def test_product_detail_view(client, product):
    path = product.get_absolute_url()

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "search_type, expected_status",
    [
        ("product", HTTPStatus.FOUND),
        ("product_type", HTTPStatus.FOUND),
        ("nonexistent", HTTPStatus.BAD_REQUEST),
    ],
)
def test_search_redirect_view(client, search_type, expected_status):
    params = {
        "search_query": "coffee",
        "search_type": search_type,
    }
    query_string = urlencode(params)
    path = reverse("products:search-redirect") + "?" + query_string

    response = client.get(path)

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_queries, search_type, expected_results",
    [
        (["cOfF", "Coffee AnD cOFFee-reLATeD"], "product_type", True),
        (["nonexistent_search_query"], "product_type", False),
        (["cOfF", "ThE BeSt roASTinG!"], "product", True),
        (["nonexistent_search_query"], "product", False),
    ],
)
def test_search_list_view(client, search_queries, search_type, expected_results):
    mixer.blend(
        "products.ProductType",
        name="Coffee",
        description="Coffee and coffee-related products.",
    )
    mixer.blend(
        "products.Product", name="Coffee", card_description="The best roasting!"
    )

    for search_query in search_queries:
        params = {
            "search_query": search_query,
            "search_type": search_type,
        }
        query_string = urlencode(params)

        url_mapping = {
            "product_type": "products:product-type-search",
            "product": "products:product-search",
        }

        path = reverse(url_mapping[search_type]) + "?" + query_string

        response = client.get(path)

        assert response.status_code == HTTPStatus.OK
        assert bool(response.context_data["object_list"]) is expected_results


if __name__ == "__main__":
    pytest.main()
