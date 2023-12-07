import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker

from api.common.tests import (
    ListTest,
    CreateTest,
    UpdateTest,
    DestroyTest,
    RetrieveTest,
)
from api.utils.tests import generate_test_image
from api.v1.categories.models import Category

User = get_user_model()


class TestCategoryViewSet:
    PRODUCT_TYPES_LIST_PATTERN = "api:v1:categories:categories-list"

    @pytest.mark.django_db
    def test_retrieve(self, client, category: Category):
        assert category.views == 0
        RetrieveTest(
            client,
            category.get_absolute_url(),
        ).run_test(
            expected_fields=(
                "id",
                "image",
                "name",
                "description",
                "views",
                "slug",
                "calories_avg",
                "protein_avg",
                "fat_avg",
                "carbs_avg",
            ),
        )
        category.refresh_from_db()
        assert category.views == 1

    @pytest.mark.django_db
    def test_list(self, client, categories: list[Category]):
        path = reverse(self.PRODUCT_TYPES_LIST_PATTERN)

        ListTest(client, path).run_test(expected_count=len(categories))

    @pytest.mark.django_db
    def test_create(self, client, admin_user: User, faker: Faker):
        path = reverse(self.PRODUCT_TYPES_LIST_PATTERN)
        data = {
            "name": faker.name(),
            "image": generate_test_image(),
            "description": faker.text(),
        }

        CreateTest(client, path, admin_user).run_test(
            model=Category,
            data=data,
        )

    @pytest.mark.django_db
    def test_update(self, client, category: Category, admin_user: User, faker: Faker):
        data = {
            "name": faker.name(),
            "description": faker.text(),
        }

        UpdateTest(
            client,
            category.get_absolute_url(),
            admin_user,
        ).run_test(
            object_to_update=category,
            data=data,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, category: Category, admin_user: User):
        DestroyTest(
            client,
            category.get_absolute_url(),
            admin_user,
        ).run_test(Category)


if __name__ == "__main__":
    pytest.main()
