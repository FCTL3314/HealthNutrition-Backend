from typing import TypeVar

import pytest
from mixer.backend.django import mixer

from api.v1.products.constants import PRICE_ROUNDING
from api.v1.products.models import Product, ProductType


@pytest.mark.django_db
def test_product_manager_price_aggregation(products: list[Product]):
    prices = [product.price for product in products]

    expected_min_price = round(min(prices), PRICE_ROUNDING)
    expected_max_price = round(max(prices), PRICE_ROUNDING)
    expected_avg_price = round(sum(prices) / len(prices), PRICE_ROUNDING)

    aggregations = Product.objects.all().price_aggregation()

    assert aggregations["price__min"] == pytest.approx(expected_min_price)
    assert aggregations["price__max"] == pytest.approx(expected_max_price)
    assert aggregations["price__avg"] == pytest.approx(expected_avg_price)


AnnotatedProductT = TypeVar("AnnotatedProductT", bound=Product)


def _get_annotated_product_type(identifier: int) -> ProductType:
    queryset = ProductType.objects.filter(id=identifier)
    annotated_queryset = queryset.products_price_annotation()
    return annotated_queryset.first()


def _get_products_aggregations(product_type: ProductType) -> dict:
    queryset = product_type.product_set.all()
    return queryset.price_aggregation()


@pytest.mark.django_db
def test_product_type_manager_price_annotation(product_type: ProductType):
    mixer.cycle(5).blend("products.Product", product_type=product_type)

    annotated_product_type = _get_annotated_product_type(product_type.id)

    products_aggregations = _get_products_aggregations(annotated_product_type)

    assert annotated_product_type.product__price__min == products_aggregations["price__min"]  # type: ignore
    assert annotated_product_type.product__price__max == products_aggregations["price__max"]  # type: ignore
    assert annotated_product_type.product__price__avg == products_aggregations["price__avg"]  # type: ignore


if __name__ == "__main__":
    pytest.main()
