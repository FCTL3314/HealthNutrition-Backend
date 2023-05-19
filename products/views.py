from urllib.parse import urlencode

from django.core.exceptions import BadRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import Product, ProductType
from utils.common.views import PaginationUrlMixin, TitleMixin


class BaseProductView(TitleMixin, FormMixin, ListView):
    form_class = SearchForm

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search_query')
        self.search_type = self.request.GET.get('search_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['search_query'] = self.search_query
        kwargs['search_type'] = self.search_type
        return kwargs


class IndexListView(BaseProductView):
    template_name = 'products/index.html'
    queryset = ProductType.objects.popular()[:12]


class ProductListView(PaginationUrlMixin, BaseProductView):
    model = ProductType
    template_name = 'products/products.html'
    paginate_by = 1
    ordering = ('name',)

    def dispatch(self, request, *args, **kwargs):
        product_type_slug = kwargs.get('product_type')
        self.product_type = get_object_or_404(self.model, slug=product_type_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.product_type.increment_views()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        result = self.product_type.product_set.prefetch_related('store')
        return result.order_by(*self.ordering)

    def get_title(self):
        return self.product_type.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_type'] = self.product_type
        return context


class SearchListView(PaginationUrlMixin, BaseProductView):
    template_name = 'products/search.html'
    title = 'Search'
    paginate_by = 1
    ordering = ('name',)

    def get_queryset(self):
        if self.search_type == 'product':
            model = Product
        elif self.search_type == 'product_type':
            model = ProductType
        else:
            raise BadRequest('Invalid search type')
        queryset = model.objects.filter(
            Q(name__icontains=self.search_query) | Q(description__icontains=self.search_query),
        )
        return queryset.order_by(*self.ordering)

    def get_pagination_url(self):
        params = {'search_query': self.search_query, 'search_type': self.search_type, 'page': ''}
        return '?' + urlencode(params)
