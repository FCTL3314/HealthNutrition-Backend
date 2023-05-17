from django.shortcuts import get_list_or_404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import Product, ProductType
from utils.common.views import TitleMixin


class IndexListView(TitleMixin, FormMixin, ListView):
    model = ProductType
    form_class = SearchForm
    template_name = 'products/index.html'


class ProductListView(TitleMixin, FormMixin, ListView):
    model = Product
    form_class = SearchForm
    template_name = 'products/products.html'
    title = 'Products'
    paginate_by = 12
    ordering = 'price'

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type = self.kwargs.get('product_type')
        return get_list_or_404(queryset.filter(product_type__slug=product_type))
