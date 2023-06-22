from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.v1.products.paginators import (ProductPageNumberPagination,
                                        ProductTypePageNumberPagination)
from api.v1.products.serializers import (ProductModelSerializer,
                                         ProductTypeModelSerializer)
from products.models import Product, ProductType


class ProductTypeModelViewSet(ModelViewSet):
    queryset = ProductType.objects.cached()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"
