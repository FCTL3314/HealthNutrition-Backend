import pytest
from mixer.backend.django import mixer

from api.v1.products.constants import PRICE_ROUNDING
from api.v1.products.models import Product, ProductType


class TestProductTypeManager:
    @pytest.mark.django_db
    def test_price_aggregation(self, products: list[Product]):
        prices = Product.objects.values_list("price", flat=True)

        expected_min_price = round(min(prices), PRICE_ROUNDING)
        expected_max_price = round(max(prices), PRICE_ROUNDING)
        expected_avg_price = round(sum(prices) / len(prices), PRICE_ROUNDING)

        aggregations = Product.objects.price_aggregation()

        assert aggregations["price__min"] == pytest.approx(expected_min_price)
        assert aggregations["price__max"] == pytest.approx(expected_max_price)
        assert aggregations["price__avg"] == pytest.approx(expected_avg_price)

    @pytest.mark.django_db
    def test_price_annotation(self, product_type: ProductType):
        mixer.cycle(5).blend("products.Product", product_type=product_type)

        product_type = ProductType.objects.products_annotation().first()
        products_aggregations = product_type.product_set.price_aggregation()

        assert product_type.product__price__min == products_aggregations["price__min"]
        assert product_type.product__price__max == products_aggregations["price__max"]
        assert product_type.product__price__avg == products_aggregations["price__avg"]


if __name__ == "__main__":
    pytest.main()
