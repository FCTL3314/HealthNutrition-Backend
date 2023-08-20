from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.v1.stores.constants import STORES_ORDERING
from api.v1.stores.models import Store
from api.v1.stores.paginators import StorePageNumberPagination
from api.v1.stores.serializers import StoreSerializer


class StoreModelViewSet(ModelViewSet):
    queryset = Store.objects.order_by(*STORES_ORDERING)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = StoreSerializer
    pagination_class = StorePageNumberPagination
    lookup_field = "slug"
