from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from common.views import (ObjectListInfoMixin, PaginationUrlMixin,
                          SearchWithSearchTypeFormMixin, TitleMixin)
from products.models import Product, ProductType


class BaseComparisonView(LoginRequiredMixin, PaginationUrlMixin, TitleMixin, ObjectListInfoMixin,
                         SearchWithSearchTypeFormMixin, ListView):
    """A base view for the 'comparisons' application."""

    title = 'Comparisons'
    object_list_title = 'My Comparison'
    object_list_description = 'Products you have saved for comparison.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comparison'] = True
        return context


class ComparisonProductTypeListView(BaseComparisonView):
    model = ProductType
    ordering = settings.PRODUCT_TYPES_ORDERING
    paginate_by = settings.PRODUCT_TYPES_PAGINATE_BY
    template_name = 'products/product_types.html'

    def get_queryset(self):
        comparisons = self.request.user.comparison_set.all()
        product_types_id = comparisons.values_list('product__product_type', flat=True).distinct()
        product_types = self.model.objects.filter(id__in=product_types_id)
        queryset = product_types.product_price_annotation()
        return queryset.order_by(*self.ordering)


class ComparisonProductListView(BaseComparisonView):
    model = Product
    ordering = settings.PRODUCTS_ORDERING
    paginate_by = settings.PRODUCTS_PAGINATE_BY
    template_name = 'products/products.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        product_type = get_object_or_404(ProductType, slug=slug)
        products = product_type.cached_products()
        queryset = products.filter(user=self.request.user)
        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context
