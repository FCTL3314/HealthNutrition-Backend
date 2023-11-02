from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from api.utils.tests import get_auth_header
from api.v1.comparisons.models import Comparison
from api.v1.comparisons.tests.conftest import create_user_comparisons
from api.v1.products.models import Product

User = get_user_model()

COMPARISON_ADD_PATTERN = "api:v1:comparisons:add"
COMPARISON_REMOVE_PATTERN = "api:v1:comparisons:remove"

COMPARISON_PRODUCT_TYPES_PATTERN = "api:v1:comparisons:product-types"
COMPARISON_PRODUCTS_PATTERN = "api:v1:comparisons:products"


def _is_comparison_exists(user: User, product: Product):
    return Comparison.objects.filter(
        user=user,
        product=product,
    ).exists()


@pytest.mark.django_db
def test_comparison_create_view(client, product: Product, admin_user: User):
    path = reverse(COMPARISON_ADD_PATTERN, args=(product.id,))

    response = client.post(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.CREATED
    assert _is_comparison_exists(admin_user, product)


@pytest.mark.django_db
def test_comparison_remove_view(client, product: Product, admin_user: User):
    Comparison.objects.create(user=admin_user, product=product)
    assert _is_comparison_exists(admin_user, product)

    path = reverse(COMPARISON_REMOVE_PATTERN, args=(product.id,))

    response = client.delete(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not _is_comparison_exists(admin_user, product)


@pytest.mark.django_db
def test_compared_product_types_list_view(client, admin_user: User):
    create_user_comparisons(admin_user)
    path = reverse(COMPARISON_PRODUCT_TYPES_PATTERN)

    response = client.get(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.OK
    assert len(response.data["results"]) > 0


@pytest.mark.django_db
def test_compared_products_list_view(client, admin_user: User):
    comparisons = create_user_comparisons(admin_user)
    product_type = comparisons[0].product.product_type
    path = reverse(COMPARISON_PRODUCTS_PATTERN, args=(product_type.slug,))

    response = client.get(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.OK
    assert len(response.data["results"]) > 0


if __name__ == "__main__":
    pytest.main()
