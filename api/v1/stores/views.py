from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.responses import APIResponse
from api.utils.network import get_client_address
from api.v1.stores.constants import STORES_ORDERING
from api.v1.stores.models import Store
from api.v1.stores.paginators import StorePageNumberPagination
from api.v1.stores.serializers import StoreSerializer
from api.v1.stores.services.domain import StoreViewsIncreaseService
from api.v1.stores.services.infrastructure import StoreRetrieveService


class StoreModelViewSet(ModelViewSet):
    queryset = Store.objects.order_by(*STORES_ORDERING)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = StoreSerializer
    pagination_class = StorePageNumberPagination
    lookup_field = "slug"

    def retrieve(self, request: Request, *args, **kwargs) -> APIResponse:
        instance = self.get_object()
        return StoreRetrieveService(
            instance,
            self.serializer_class,
            StoreViewsIncreaseService(instance, get_client_address(request)),
        ).retrieve()
