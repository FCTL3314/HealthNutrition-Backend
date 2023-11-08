from django_filters import rest_framework as filters

from api.v1.products.models import Product


class ProductFilter(filters.FilterSet):
    category_slug = filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Product
        fields = ("category__slug",)
