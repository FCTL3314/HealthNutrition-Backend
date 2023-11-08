from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.base.services import (
    BaseViewsIncreaseService,
    IRetrieveService,
    AbstractConditionalIncreaseService,
)
from api.responses import APIResponse
from api.v1.categories.models import Category
from api.v1.categories.constants import CATEGORY_VIEW_CACHE_TIME


class CategoryViewsIncreaseService(BaseViewsIncreaseService):
    view_cache_time = CATEGORY_VIEW_CACHE_TIME

    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_type_id:{self._instance.id}"


class CategoryRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Category,
        serializer: type[Serializer],
        views_increase_service: AbstractConditionalIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_increase_service = views_increase_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_increase_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
