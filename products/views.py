from urllib.parse import urlencode

from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import Product, ProductType
from utils.common.views import PaginationUrlMixin, TitleMixin


class BaseProductsView(TitleMixin, PaginationUrlMixin, FormMixin, ListView):
    template_name = 'products/index.html'
    form_class = SearchForm
    paginate_by = 12

    object_list_title = ''
    object_list_description = ''

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search_query', '')
        self.search_type = self.request.GET.get('search_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['search_query'] = self.search_query
        kwargs['search_type'] = self.search_type
        return kwargs

    def get_object_list_title(self):
        return self.object_list_title

    def get_object_list_description(self):
        return self.object_list_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list_title'] = self.get_object_list_title()
        context['object_list_description'] = self.get_object_list_description()
        context['search_query'] = self.search_query
        context['search_type'] = self.search_type
        return context


class ProductTypeListView(BaseProductsView):
    ordering = ('views',)
    title = 'Categories'
    object_list_title = 'Featured Categories'
    object_list_description = 'Categories of products that users open most often.'

    def get_queryset(self):
        initial_queryset = ProductType.objects.popular()
        queryset = initial_queryset.product_statistic_annotation()
        return queryset.order_by(*self.ordering)


class ProductListView(BaseProductsView):
    model = ProductType
    ordering = ('price',)
    object_list_description = 'List of products based on the category you selected.'

    def dispatch(self, request, *args, **kwargs):
        product_type_slug = kwargs.get('slug')
        self.product_type = get_object_or_404(self.model, slug=product_type_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.product_type.increment_views()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        initial_queryset = self.product_type.product_set.all()
        queryset = initial_queryset.prefetch_related('store')
        return queryset.order_by(*self.ordering)

    def get_title(self):
        return self.product_type.name

    def get_object_list_title(self):
        return f'Products of category: {self.product_type.name}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context


class SearchListView(BaseProductsView):
    title = 'Search'
    object_list_title = 'Search results'
    object_list_description = 'Search results based on your query.'

    def get_queryset(self):
        if self.search_type == 'product':
            return Product.objects.search(self.search_query).order_by('price')
        elif self.search_type == 'product_type':
            queryset = ProductType.objects.search(self.search_query)
            return queryset.product_statistic_annotation().order_by('views')
        else:
            return list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.search_type == 'product':
            context.update(self.object_list.price_aggregation())
        return context

    def get_pagination_url(self):
        return '?' + urlencode({'search_query': self.search_query, 'search_type': self.search_type, 'page': ''})
