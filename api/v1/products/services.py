from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.base.services import IRetrieveService, ViewsIncreaseService
from api.responses import APIResponse
from api.v1.products.models import Product, ProductType


class ProductViewsIncreaseService(ViewsIncreaseService):
    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_id:{self._instance.id}"


class ProductTypeViewsIncreaseService(ViewsIncreaseService):
    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_type_id:{self._instance.id}"


class ProductRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Product,
        serializer: type[Serializer],
        views_service: ViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_increase_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_increase_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)


class ProductTypeRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: ProductType,
        serializer: type[Serializer],
        views_service: ViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_increase_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_increase_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
