from django_filters import rest_framework as filters

from api.v1.products.models import Product


class ProductFilter(filters.FilterSet):
    product_type_slug = filters.CharFilter(
        field_name="product_type__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Product
        fields = ("product_type__slug",)
