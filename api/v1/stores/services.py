from http import HTTPStatus

from rest_framework.serializers import Serializer

from api.base.services import IRetrieveService, ViewsIncreaseService
from api.responses import APIResponse
from api.v1.stores.models import Store


class StoreViewsIncreaseService(ViewsIncreaseService):
    def get_cache_key(self) -> str:
        return f"address:{self._user_ip_address}-store_id:{self._instance.id}"


class StoreRetrieveService(IRetrieveService):
    def __init__(
        self,
        instance: Store,
        serializer: type[Serializer],
        views_service: ViewsIncreaseService,
    ):
        super().__init__(instance, serializer)
        self._views_service = views_service

    def retrieve(self, *args, **kwargs) -> APIResponse:
        self._views_service._increase()
        serializer = self._serializer(self._instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
