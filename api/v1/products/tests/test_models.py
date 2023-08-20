import pytest
from mixer.backend.django import mixer

from api.v1.products.constants import PRICE_ROUNDING
from api.v1.products.models import Product, ProductType


@pytest.mark.django_db
def test_product_manager_price_aggregation(products: list[Product]):
    ids = []
    prices = []

    for product in products:
        ids.append(product.id)
        prices.append(product.price)

    min_price = round(min(prices), PRICE_ROUNDING)
    max_price = round(max(prices), PRICE_ROUNDING)
    avg_price = round(sum(prices) / len(prices), PRICE_ROUNDING)

    queryset = Product.objects.filter(id__in=ids)
    aggregations = queryset.price_aggregation()

    assert aggregations["price__min"] == pytest.approx(min_price)
    assert aggregations["price__max"] == pytest.approx(max_price)
    assert aggregations["price__avg"] == pytest.approx(avg_price)


@pytest.mark.django_db
def test_product_type_manager_price_annotation(product_type: ProductType):
    mixer.cycle(5).blend("products.Product", product_type=product_type)
    queryset = ProductType.objects.filter(id=product_type.id)
    annotated_queryset = queryset.products_price_annotation()

    test_object = annotated_queryset.first()

    products_ids = [product.id for product in test_object.product_set.all()]
    products_queryset = Product.objects.filter(id__in=products_ids)
    products_aggregations = products_queryset.price_aggregation()

    assert test_object.product__price__min == products_aggregations["price__min"]
    assert test_object.product__price__max == products_aggregations["price__max"]
    assert test_object.product__price__avg == products_aggregations["price__avg"]


if __name__ == "__main__":
    pytest.main()
