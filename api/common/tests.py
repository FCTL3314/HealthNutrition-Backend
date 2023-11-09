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


class BaseCommonTest(ABC):
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

    @abstractmethod
    def run_test(self, *args, **kwargs):
        ...

    @property
    def headers(self) -> dict:
        return get_auth_header(self._user) if self._user else {}


class RetrieveTest(BaseCommonTest):
    def run_test(self, expected_fields: Iterable[str]):
        response = self._client.get(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.OK
        for field in expected_fields:
            assert field in response.data
        return response


class RetrieveViewsIncreaseTest(RetrieveTest):
    def __init__(
        self,
        client,
        path: str,
        model_object: ViewsModelMixin,
        user: User | None = None,
        expected_status: int | None = None,
    ):
        super().__init__(client, path, user, expected_status)
        self._model_object = model_object

    def run_test(self, expected_fields: Iterable[str]):
        assert self._model_object.views == 0
        super().run_test(expected_fields)
        self._model_object.refresh_from_db()
        assert self._model_object.views == 1


class ListTest(BaseCommonTest):
    def run_test(self, expected_count: int | None = None):
        response = self._client.get(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.OK
        objects_count = response.data["count"]
        if expected_count is not None:
            assert objects_count == expected_count
        else:
            assert objects_count > 0
        return response


class CreateTest(BaseCommonTest):
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


class UpdateTest(BaseCommonTest):
    def run_test(
        self,
        object_to_update: Model,
        data: dict[str, Any],
    ):
        response = self._client.patch(
            self._path,
            data=data,
            content_type="application/json",
            **self.headers,
        )

        object_to_update.refresh_from_db()

        assert response.status_code == self._expected_status or HTTPStatus.OK
        for field in data:
            assert getattr(object_to_update, field) == data[field]
        return response


class DestroyTest(BaseCommonTest):
    def run_test(self, model: type[Model]):
        assert model.objects.count() == 1

        response = self._client.delete(self._path, **self.headers)

        assert response.status_code == self._expected_status or HTTPStatus.NO_CONTENT
        assert model.objects.count() == 0
        return response
