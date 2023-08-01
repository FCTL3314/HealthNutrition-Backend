from common.permissions import IsAdminOrReadOnly
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from stores.models import Store
from stores.paginators import StorePageNumberPagination
from stores.serializers import StoreModelSerializer


class StoreModelViewSet(ModelViewSet):
    queryset = Store.objects.order_by(*settings.STORES_ORDERING)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = StoreModelSerializer
    pagination_class = StorePageNumberPagination
    lookup_field = "slug"
