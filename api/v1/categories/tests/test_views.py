import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from api.common.tests import (
    RetrieveViewsCommonTest,
    ListCommonTest,
    CreateCommonTest,
    UpdateCommonTest,
    DestroyCommonTest,
)
from api.utils.tests import generate_test_image
from api.v1.categories.models import Category

User = get_user_model()


class TestCategoryViewSet:
    PRODUCT_TYPES_LIST_PATTERN = "api:v1:products:product-types-list"

    @pytest.mark.django_db
    def test_retrieve(self, client, category: Category):
        path = category.get_absolute_url()

        RetrieveViewsCommonTest(client, path, category).run_test(
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
    def test_list(self, client, categories):
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
            Category,
            data,
        )

    @pytest.mark.django_db
    def test_update(self, client, category: Category, admin_user: User, faker: Faker):
        path = category.get_absolute_url()
        fields = {
            "name": faker.name(),
            "description": faker.text(),
        }

        UpdateCommonTest(client, path, admin_user).run_test(
            category,
            fields,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, category: Category, admin_user: User):
        path = category.get_absolute_url()

        DestroyCommonTest(client, path, admin_user).run_test(Category)
