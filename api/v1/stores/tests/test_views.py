import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.reverse import reverse

from api.common.tests import (
    CreateCommonTest,
    DestroyCommonTest,
    ListCommonTest,
    RetrieveCommonTest,
    UpdateCommonTest,
)
from api.utils.tests import generate_test_image
from api.v1.stores.models import Store

User = get_user_model()


class TestStoreViewSet:
    URL_PATTERN = "api:v1:stores:stores-list"
    DETAIL_URL_PATTERN = "api:v1:stores:stores-detail"

    @pytest.mark.django_db
    def test_detail(self, client, store: Store):
        path = reverse(self.DETAIL_URL_PATTERN, args=(store.slug,))

        RetrieveCommonTest(client, path).run_test(
            (
                "id",
                "name",
                "description",
                "logo",
                "url",
                "slug",
                "views",
            ),
        )

    @pytest.mark.django_db
    def test_list(self, client, stores: list[Store]):
        path = reverse(self.URL_PATTERN)

        ListCommonTest(client, path).run_test()

    @pytest.mark.django_db
    def test_create(self, client, admin_user: User, faker: Faker):
        path = reverse(self.URL_PATTERN)
        data = {
            "name": faker.name(),
            "url": faker.url(),
            "logo": generate_test_image(),
            "description": faker.text(),
        }

        CreateCommonTest(client, path, admin_user).run_test(
            Store,
            data,
        )

    @pytest.mark.django_db
    def test_update(self, client, store: Store, admin_user: User, faker: Faker):
        path = reverse(self.DETAIL_URL_PATTERN, args=(store.slug,))
        fields = {
            "name": faker.name(),
            "description": faker.text(),
        }

        UpdateCommonTest(client, path, admin_user).run_test(
            store,
            fields,
        )

    @pytest.mark.django_db
    def test_destroy(self, client, store: Store, admin_user: User):
        path = reverse(self.DETAIL_URL_PATTERN, args=(store.slug,))

        DestroyCommonTest(client, path, admin_user).run_test(Store)


if __name__ == "__main__":
    pytest.main()
