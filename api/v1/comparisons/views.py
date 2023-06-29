from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.v1.products.paginators import ProductTypePageNumberPagination
from api.v1.products.serializers import ProductTypeModelSerializer


class ComparisonProductTypeModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    def get_queryset(self):
        product_types = self.request.user.comparison_set.product_types()
        queryset = product_types.product_price_annotation()
        return queryset.order_by(*settings.PRODUCT_TYPES_ORDERING)
