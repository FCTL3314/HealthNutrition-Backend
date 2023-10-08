from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Iterable

from django.contrib.auth import get_user_model
from django.db.models import Model
from faker import Faker

from api.common.models.mixins import ViewsModelMixin
from api.utils.tests import get_auth_header

User = get_user_model()


faker = Faker()


class ICommonTest(ABC):
    @abstractmethod
    def run_test(self, *args, **kwargs):
        ...


class BaseCommonTest(ICommonTest, ABC):
    def __init__(
        self,
        client,
        path: str,
        user: User | None = None,
        expected_status: int | None = None,
    ):
        self._client = client
        self._path = path
        self._user = user
        self._expected_status = expected_status

    @property
    def headers(self) -> dict:
        return get_auth_header(self._user) if self._user else {}


class RetrieveCommonTest(BaseCommonTest):
    def run_test(self, expected_fields: Iterable[str]):
        response = self._client.get(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.OK
        for field in expected_fields:
            assert field in response.data
        return response


class RetrieveViewsCommonTest(RetrieveCommonTest):
    def __init__(
        self,
        client,
        path: str,
        views_model_object: ViewsModelMixin,
        user: User | None = None,
        expected_status: int | None = None,
    ):
        super().__init__(client, path, user, expected_status)
        self._views_model_object = views_model_object

    def run_test(self, expected_fields: Iterable[str]):
        assert self._views_model_object.views == 0
        super().run_test(expected_fields)
        self._views_model_object.refresh_from_db()
        assert self._views_model_object.views == 1


class ListCommonTest(BaseCommonTest):
    def run_test(self):
        response = self._client.get(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.OK
        assert len(response.data["results"]) > 0
        return response


class CreateCommonTest(BaseCommonTest):
    def run_test(
        self,
        model: type[Model],
        data: dict[str, Any],
    ):
        assert model.objects.count() == 0

        response = self._client.post(
            self._path,
            data=data,
            **self.headers,
        )

        assert response.status_code == self._expected_status or HTTPStatus.CREATED
        assert model.objects.count() == 1
        return response


class UpdateCommonTest(BaseCommonTest):
    def run_test(
        self,
        object_to_update: Model,
        fields: dict[str, Any],
    ):
        response = self._client.patch(
            self._path,
            data=fields,
            content_type="application/json",
            **self.headers,
        )

        object_to_update.refresh_from_db()

        assert response.status_code == self._expected_status or HTTPStatus.OK
        for field in fields:
            assert getattr(object_to_update, field) == fields[field]
        return response


class DestroyCommonTest(BaseCommonTest):
    def run_test(self, model: type[Model]):
        assert model.objects.count() == 1

        response = self._client.delete(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.NO_CONTENT
        assert model.objects.count() == 0
        return response
