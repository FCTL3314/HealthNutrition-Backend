import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from api.common.tests import (
    CreateCommonTest,
    DestroyCommonTest,
    ListCommonTest,
    RetrieveCommonTest,
    UpdateCommonTest,
)
from api.utils.tests import generate_test_image
from api.v1.products.models import ProductType

User = get_user_model()


PRODUCT_TYPE_DETAIL = "api:v1:products:product-types-detail"
PRODUCT_TYPES = "api:v1:products:product-types-list"


class TestProductTypeModelViewSet:
    @pytest.mark.django_db
    def test_retrieve(self, client, product_type: ProductType):
        path = reverse(PRODUCT_TYPE_DETAIL, args=(product_type.slug,))

        RetrieveCommonTest(client, path).run_test(
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
        path = reverse(PRODUCT_TYPES)

        ListCommonTest(client, path).run_test()

    @pytest.mark.django_db
    def test_create(self, client, admin_user: User, faker: Faker):
        path = reverse(PRODUCT_TYPES)
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
        path = reverse(PRODUCT_TYPE_DETAIL, args=(product_type.slug,))
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
        path = reverse(PRODUCT_TYPE_DETAIL, args=(product_type.slug,))

        DestroyCommonTest(client, path, admin_user).run_test(ProductType)


if __name__ == "__main__":
    pytest.main()
