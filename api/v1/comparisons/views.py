from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated

from api.decorators import order_queryset
from api.v1.comparisons.models import Comparison
from api.v1.comparisons.serializers import ComparisonSerializer
from api.v1.products.constants import PRODUCT_TYPES_ORDERING, PRODUCTS_ORDERING
from api.v1.products.models import Product, ProductType
from api.v1.products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from api.v1.products.serializers import (
    ProductSerializer,
    ProductTypeAggregatedSerializer,
)


class ComparisonCreateView(CreateAPIView):
    serializer_class = ComparisonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs["product_id"])
        serializer.save(user=self.request.user, product=product)


class ComparisonDestroyView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Product.objects.get(id=self.kwargs["product_id"])

    def perform_destroy(self, instance):
        Comparison.objects.filter(
            user=self.request.user,
            product=instance,
        ).delete()


class ComparedProductTypesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    @order_queryset(*PRODUCT_TYPES_ORDERING)
    def get_queryset(self):
        product_types = Comparison.objects.product_types(self.request.user)
        return product_types.products_price_annotation()


class ComparedProductsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination

    @order_queryset(*PRODUCTS_ORDERING)
    def get_queryset(self):
        product_type = get_object_or_404(ProductType, slug=self.kwargs["slug"])
        return Comparison.objects.products(product_type, self.request.user)
