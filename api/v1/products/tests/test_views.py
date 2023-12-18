import pytest
from django.urls import reverse
from faker import Faker

from api.common.tests import (
    CreateTest,
    DestroyTest,
    ListTest,
    UpdateTest,
    RetrieveTest,
)
from api.utils.tests import generate_test_image
from api.v1.categories.models import Category
from api.v1.categories.tests.test_views import User
from api.v1.nutrition.models import Nutrition
from api.v1.products.models import Product


class TestProductViewSet:
    PRODUCTS_LIST_PATTERN = "api:v1:products:products-list"

    @pytest.mark.django_db
    def test_retrieve(self, client, product: Product):
        assert product.views == 0
        RetrieveTest(client, product.get_absolute_url()).run_test(
            expected_fields=(
                "id",
                "image",
                "name",
                "short_description",
                "nutrition",
                "category",
                "healthfulness",
                "views",
                "slug",
                "created_at",
                "updated_at",
            ),
        )
        product.refresh_from_db()
        assert product.views == 1

    @pytest.mark.django_db
    def test_list(self, client, products: list[Product]):
        path = reverse(self.PRODUCTS_LIST_PATTERN)
        ListTest(client, path).run_test(expected_count=len(products))

    @pytest.mark.django_db
    def test_create(
        self,
        client,
        nutrition: Nutrition,
        category: Category,
        admin_user: User,
        faker: Faker,
    ):
        path = reverse(self.PRODUCTS_LIST_PATTERN)
        data = {
            "name": faker.name(),
            "image": generate_test_image(),
            "short_description": faker.text(
                Product._meta.get_field("short_description").max_length,
            ),
            "description": faker.text(),
            "nutrition_id": nutrition.id,
            "category_id": category.id,
        }

        CreateTest(client, path, admin_user).run_test(
            model=Product,
            data=data,
        )

    @pytest.mark.django_db
    def test_update(self, client, product: Product, admin_user: User, faker: Faker):
        data = {
            "name": faker.name(),
            "short_description": faker.text(
                Product._meta.get_field("short_description").max_length,
            ),
        }

        UpdateTest(
            client,
            product.get_absolute_url(),
            admin_user,
        ).run_test(
            object_to_update=product,
            data=data,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, product: Product, admin_user: User):
        DestroyTest(
            client,
            product.get_absolute_url(),
            admin_user,
        ).run_test(model=Product)


if __name__ == "__main__":
    pytest.main()
