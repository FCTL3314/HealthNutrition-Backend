from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from products.forms import SearchForm
from products.models import Product, ProductType
from utils.common.views import TitleMixin


class IndexTemplateView(TitleMixin, FormMixin, TemplateView):
    form_class = SearchForm
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_categories'] = ProductType.objects.order_by('-views')
        return context


class ProductListView(TitleMixin, FormMixin, ListView):
    model = Product
    form_class = SearchForm
    template_name = 'products/products.html'
    paginate_by = 12
    ordering = 'price'

    def dispatch(self, request, *args, **kwargs):
        product_type_slug = kwargs.get('product_type')
        self.product_type = get_object_or_404(ProductType, slug=product_type_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.product_type.increment_views()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return get_list_or_404(queryset.filter(product_type=self.product_type))

    def get_title(self):
        return self.product_type.name

    def _get_pagination_url(self):
        return reverse('products:products', args=(self.product_type.slug,)) + '?page='

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type'] = self.product_type
        context['pagination_url'] = self._get_pagination_url()
        return context
