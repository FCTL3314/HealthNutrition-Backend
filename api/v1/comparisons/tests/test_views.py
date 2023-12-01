from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from api.utils.tests import get_auth_header
from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.tests.conftest import create_comparisons_for_comparison_group
from api.v1.products.models import Product

User = get_user_model()


def _is_comparison_exists(comparison_group: ComparisonGroup, product: Product) -> bool:
    return Comparison.objects.filter(
        comparison_group=comparison_group,
        product=product,
    ).exists()


@pytest.mark.django_db
def test_compared_products_list_view(
    client,
    comparison_group: ComparisonGroup,
    user: User,
):
    comparisons = create_comparisons_for_comparison_group(comparison_group.id)
    path = reverse("api:v1:comparisons:list")

    response = client.get(
        path,
        **get_auth_header(user),
        data={
            "comparison_group_id": comparison_group.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data["count"] == len(comparisons)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_comparison_group_author, expected_status",
    [
        (True, HTTPStatus.CREATED),
        (False, HTTPStatus.FORBIDDEN),
    ],
)
def test_comparison_create_view(
    client,
    comparison_group: ComparisonGroup,
    product: Product,
    user: User,
    is_comparison_group_author: bool,
    expected_status: HTTPStatus,
):
    """
    Tests the ability to add a product to a
    comparison group if the user is the author
    of this comparison group.
    """
    path = reverse("api:v1:comparisons:add")
    data = {
        "product_id": product.id,
        "comparison_group_id": comparison_group.id,
    }

    if is_comparison_group_author:
        user = comparison_group.author

    response = client.post(path, data=data, **get_auth_header(user))

    assert response.status_code == expected_status
    if expected_status == HTTPStatus.CREATED:
        assert _is_comparison_exists(comparison_group, product)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_comparison_group_author, expected_status",
    [
        (True, HTTPStatus.NO_CONTENT),
        (False, HTTPStatus.FORBIDDEN),
    ],
)
def test_comparison_remove_view(
    client,
    comparison_group: ComparisonGroup,
    product: Product,
    user: User,
    is_comparison_group_author: bool,
    expected_status: HTTPStatus,
):
    """
    Tests the ability to remove a product to a
    comparison group if the user is the author
    of this comparison group.
    """
    if is_comparison_group_author:
        user = comparison_group.author

    Comparison.objects.create(
        creator=comparison_group.author,
        product=product,
        comparison_group=comparison_group,
    )
    assert _is_comparison_exists(comparison_group, product)

    path = reverse("api:v1:comparisons:remove")
    data = {
        "product_id": product.id,
        "comparison_group_id": comparison_group.id,
    }

    response = client.delete(
        path,
        data=data,
        content_type="application/json",
        **get_auth_header(user),
    )

    assert response.status_code == expected_status
    if expected_status == HTTPStatus.NO_CONTENT:
        assert not _is_comparison_exists(comparison_group, product)


if __name__ == "__main__":
    pytest.main()
