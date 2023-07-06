from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from products.forms import SearchForm
from products.mixins import SearchFormMixin
from common import mixins as common_views
from common.decorators import order_queryset
from products.models import ProductType


class BaseComparisonView(
    LoginRequiredMixin,
    common_views.PaginationUrlMixin,
    common_views.TitleMixin,
    common_views.ObjectListInfoMixin,
    SearchFormMixin,
    ListView,
):
    """A base view for the 'comparisons' application."""

    title = "Comparisons"
    form_class = SearchForm
    object_list_title = "My Comparison"
    object_list_description = "Products you have saved for comparison."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comparison"] = True
        return context


class ComparisonProductTypeListView(BaseComparisonView):
    ordering = settings.PRODUCT_TYPES_ORDERING
    paginate_by = settings.PRODUCT_TYPES_PAGINATE_BY
    template_name = "products/product_types.html"

    @order_queryset(*ordering)
    def get_queryset(self):
        product_types = self.request.user.comparison_set.product_types()
        return product_types.product_price_annotation()


class ComparisonProductListView(BaseComparisonView):
    ordering = settings.PRODUCTS_ORDERING
    paginate_by = settings.PRODUCTS_PAGINATE_BY
    template_name = "products/products.html"

    @order_queryset(*ordering)
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        product_type = get_object_or_404(ProductType, slug=slug)
        products = product_type.cached_products()
        return products.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context
