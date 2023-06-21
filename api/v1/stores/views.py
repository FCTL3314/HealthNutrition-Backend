from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.v1.stores.paginators import StorePageNumberPagination
from api.v1.stores.serializers import StoreModelSerializer
from stores.models import Store


class StoreModelViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreModelSerializer
    pagination_class = StorePageNumberPagination
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ("create", "update", "destroy"):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
