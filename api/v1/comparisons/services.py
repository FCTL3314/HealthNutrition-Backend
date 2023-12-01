from http import HTTPStatus
from typing import Any

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.base.services import IService
from api.responses import APIResponse
from api.utils.errors import Error
from api.v1.comparisons.models import Comparison

User = get_user_model()


class ComparisonCreateErrors:
    PRODUCT_ALREADY_ADDED = Error(
        "This product has already been added to this comparison group",
        "product_already_added",
    )


class ComparisonCreateService(IService):
    def __init__(
        self,
        serializer_class: type[Serializer],
        data: dict[str, Any],
        user: User,
    ):
        self._serializer = serializer_class(data=data)
        self._serializer.is_valid(raise_exception=True)
        self._comparison_group_id = data["comparison_group_id"]
        self._product_id = data["product_id"]
        self._user = user

    def execute(self) -> Response | APIResponse:
        if self._is_comparison_already_exists():
            return self._product_already_added_response()
        self._serializer.save(creator=self._user)
        return self._successfully_created_response()

    def _is_comparison_already_exists(self) -> bool:
        return Comparison.objects.filter(
            comparison_group_id=self._comparison_group_id, product_id=self._product_id
        ).exists()

    def _successfully_created_response(self):
        return Response(self._serializer.data, status=HTTPStatus.CREATED)

    @classmethod
    def _product_already_added_response(cls) -> APIResponse:
        return APIResponse(
            detail=ComparisonCreateErrors.PRODUCT_ALREADY_ADDED.message,
            code=ComparisonCreateErrors.PRODUCT_ALREADY_ADDED.code,
            status=HTTPStatus.BAD_REQUEST,
        )


class ComparisonDeleteService(IService):
    def __init__(self, serializer_class: type[Serializer], data: dict[str, Any]):
        self._serializer = serializer_class(data=data)
        self._serializer.is_valid(raise_exception=True)
        self._comparison_group_id = data["comparison_group_id"]
        self._product_id = data["product_id"]

    def execute(self) -> Response:
        instance = get_object_or_404(
            Comparison,
            comparison_group_id=self._comparison_group_id,
            product_id=self._product_id,
        )
        instance.delete()
        return self._successfully_deleted_response()

    @classmethod
    def _successfully_deleted_response(cls) -> Response:
        return Response(status=HTTPStatus.NO_CONTENT)
