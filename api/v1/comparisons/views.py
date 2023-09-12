from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated

from api.decorators import order_queryset
from api.v1.comparisons.docs import (
    comparison_create_view_docs,
    comparison_delete_view_docs,
)
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


@comparison_create_view_docs()
class ComparisonCreateView(CreateAPIView):
    serializer_class = ComparisonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs["product_id"])
        serializer.save(user=self.request.user, product=product)


@comparison_delete_view_docs()
class ComparisonDestroyView(DestroyAPIView):
    model = Comparison
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Product.objects.get(id=self.kwargs["product_id"])

    def perform_destroy(self, instance):
        self.model.objects.filter(
            user=self.request.user,
            product=instance,
        ).delete()


class ComparedProductTypesListView(ListAPIView):
    queryset = Comparison.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    @order_queryset(*PRODUCT_TYPES_ORDERING)
    def get_queryset(self):
        product_types = self.queryset.product_types(self.request.user)
        return product_types.products_annotation()


class ComparedProductsListView(ListAPIView):
    queryset = Comparison.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination

    @order_queryset(*PRODUCTS_ORDERING)
    def get_queryset(self):
        product_type = get_object_or_404(
            ProductType, slug=self.kwargs["product_type_slug"]
        )
        return self.queryset.products(product_type, self.request.user)
