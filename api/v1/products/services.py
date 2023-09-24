from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.common.services.base import IRetrieveService
from api.common.services.models import CachedViewsIncreaseService
from api.responses import APIResponse
from api.v1.products.models import Product, ProductType


class ProductViewsIncreaseService(CachedViewsIncreaseService):
    def get_cache_key(self) -> str:
        return f"address:{self._address}-product_id:{self._instance.id}"


class ProductTypeViewsIncreaseService(CachedViewsIncreaseService):
    def get_cache_key(self) -> str:
        return f"address:{self._address}-product_type_id:{self._instance.id}"


class ProductRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Product,
        serializer: type[Serializer],
        views_service: CachedViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_service.increase()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)


class ProductTypeRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: ProductType,
        serializer: type[Serializer],
        views_service: CachedViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_service.increase()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
