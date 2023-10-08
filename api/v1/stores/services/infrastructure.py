from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.base.services import IRetrieveService, BaseViewsIncreaseService
from api.responses import APIResponse
from api.v1.stores.models import Store


class StoreRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Store,
        serializer: type[Serializer],
        views_service: BaseViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_service.execute()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
