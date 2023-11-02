import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from api.common.tests import (
    CreateCommonTest,
    DestroyCommonTest,
    ListCommonTest,
    RetrieveViewsCommonTest,
    UpdateCommonTest,
)
from api.utils.tests import generate_test_image
from api.v1.products.models import Product, ProductType
from api.v1.stores.models import Store

User = get_user_model()


class TestProductTypeViewSet:
    PRODUCT_TYPES_LIST_PATTERN = "api:v1:products:product-types-list"

    @pytest.mark.django_db
    def test_retrieve(self, client, product_type: ProductType):
        path = product_type.get_absolute_url()

        RetrieveViewsCommonTest(client, path, product_type).run_test(
            (
                "id",
                "name",
                "description",
                "image",
                "views",
                "slug",
                "product_price_max",
                "product_price_avg",
                "product_price_min",
                "product_stores_count",
            ),
        )

    @pytest.mark.django_db
    def test_list(self, client, product_types: list[ProductType]):
        path = reverse(self.PRODUCT_TYPES_LIST_PATTERN)

        ListCommonTest(client, path).run_test()

    @pytest.mark.django_db
    def test_create(self, client, admin_user: User, faker: Faker):
        path = reverse(self.PRODUCT_TYPES_LIST_PATTERN)
        data = {
            "name": faker.name(),
            "description": faker.text(),
            "image": generate_test_image(),
        }

        CreateCommonTest(client, path, admin_user).run_test(
            ProductType,
            data,
        )

    @pytest.mark.django_db
    def test_update(
        self, client, product_type: ProductType, admin_user: User, faker: Faker
    ):
        path = product_type.get_absolute_url()
        fields = {
            "name": faker.name(),
            "description": faker.text(),
        }

        UpdateCommonTest(client, path, admin_user).run_test(
            product_type,
            fields,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, product_type: ProductType, admin_user: User):
        path = product_type.get_absolute_url()

        DestroyCommonTest(client, path, admin_user).run_test(ProductType)


class TestProductViewSet:
    PRODUCTS_LIST_PATTERN = "api:v1:products:products-list"

    @pytest.mark.django_db
    def test_retrieve(self, client, product: Product):
        path = product.get_absolute_url()

        assert product.views == 0
        RetrieveViewsCommonTest(client, path, product).run_test(
            (
                "id",
                "name",
                "description",
                "card_description",
                "image",
                "views",
                "slug",
                "price",
                "created_at",
                "updated_at",
                "store",
                "product_type",
            ),
        )
        product.refresh_from_db()
        assert product.views == 1

    @pytest.mark.django_db
    def test_list(self, client, products: list[Product]):
        path = reverse(self.PRODUCTS_LIST_PATTERN)

        ListCommonTest(client, path).run_test()

    @pytest.mark.django_db
    def test_create(
        self,
        client,
        product_type: ProductType,
        store: Store,
        admin_user: User,
        faker: Faker,
    ):
        path = reverse(self.PRODUCTS_LIST_PATTERN)
        data = {
            "name": faker.name(),
            "price": faker.pyfloat(2, 2, positive=True),
            "description": faker.text(),
            "card_description": faker.text(64),
            "store_id": store.id,
            "product_type_id": product_type.id,
            "image": generate_test_image(),
        }

        CreateCommonTest(client, path, admin_user).run_test(
            Product,
            data,
        )

    @pytest.mark.django_db
    def test_update(self, client, product: Product, admin_user: User, faker: Faker):
        path = product.get_absolute_url()
        fields = {
            "name": faker.name(),
            "price": faker.pyfloat(2, 2, positive=True),
            "description": faker.text(),
            "card_description": faker.text(64),
        }

        UpdateCommonTest(client, path, admin_user).run_test(
            product,
            fields,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, product: Product, admin_user: User):
        path = product.get_absolute_url()

        DestroyCommonTest(client, path, admin_user).run_test(Product)


if __name__ == "__main__":
    pytest.main()
