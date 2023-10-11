from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.base.services import IRetrieveService, AbstractConditionalIncreaseService
from api.responses import APIResponse
from api.v1.products.models import Product, ProductType


class ProductRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Product,
        serializer: type[Serializer],
        views_increase_service: AbstractConditionalIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_increase_service = views_increase_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_increase_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)


class ProductTypeRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: ProductType,
        serializer: type[Serializer],
        views_increase_service: AbstractConditionalIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_increase_service = views_increase_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_increase_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
