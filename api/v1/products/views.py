from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.v1.products.paginators import ProductTypePageNumberPagination
from api.v1.products.serializers import ProductTypeModelSerializer
from products.models import ProductType


class ProductTypeModelViewSet(ModelViewSet):
    queryset = ProductType.objects.cached()
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ("create", "update", "destroy"):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
