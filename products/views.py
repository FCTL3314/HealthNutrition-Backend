from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from common.mixins import PaginationUrlMixin, TitleMixin, UserViewTrackingMixin
from interactions.forms import ProductCommentForm
from products.forms import SearchForm
from products.models import Product, ProductType


class BaseProductsView(TitleMixin, PaginationUrlMixin, FormMixin, ListView):
    template_name = 'products/index.html'
    form_class = SearchForm
    paginate_by = settings.PRODUCTS_PAGINATE_BY

    search_query: str
    search_type: str

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
    title = 'Categories'
    ordering = ('-views',)
    object_list_title = 'Discover Popular Product Categories'
    object_list_description = 'Explore our curated list of popular product categories, sorted by their popularity ' \
                              'among users.'

    def get_queryset(self):
        initial_queryset = ProductType.objects.popular()
        queryset = initial_queryset.product_price_annotation()
        return queryset.order_by(*self.ordering)


class ProductListView(UserViewTrackingMixin, BaseProductsView):
    model = ProductType
    ordering = ('store__name', 'price',)
    object_list_description = 'Discover a wide range of products available in the selected category.'

    view_tracking_cache_time = 60 * 30

    product_type: ProductType

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        self.product_type = get_object_or_404(self.model, slug=slug)
        return super().dispatch(request, *args, **kwargs)

    def get_view_tracking_cache_key(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return settings.PRODUCT_TYPE_VIEW_TRACKING_CACHE_KEY.format(addr=remote_addr, id=self.product_type.id)

    def user_not_viewed(self):
        self.product_type.increment_views()

    def get_queryset(self):
        queryset = self.product_type.get_products_with_stores()
        return queryset.order_by(*self.ordering)

    def get_title(self):
        return self.product_type.name

    def get_object_list_title(self):
        return f'Products in the category "{self.product_type.name}"'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aggregations'] = self.object_list.price_aggregation()
        return context


class ProductDetailView(TitleMixin, UserViewTrackingMixin, FormMixin, DetailView):
    model = Product
    form_class = ProductCommentForm
    template_name = 'products/product_detail.html'

    view_tracking_cache_time = 60 * 30

    def get_view_tracking_cache_key(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return settings.PRODUCT_VIEW_TRACKING_CACHE_KEY.format(addr=remote_addr, id=self.object.id)

    def user_not_viewed(self):
        self.object.increment_views()

    def get_title(self):
        return self.object.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = self.object.productcomment_set.order_by('-created_at')
        comments_count = comments.count()

        context['comments'] = comments[:settings.COMMENTS_PAGINATE_BY]
        context['comments_count'] = comments_count
        context['has_more_comments'] = comments_count > settings.COMMENTS_PAGINATE_BY
        return context


class SearchListView(BaseProductsView):
    title = 'Search'
    object_list_title = 'Search results'
    object_list_description = 'Discover the results of your search query.'

    def get_queryset(self):
        queryset = list()
        if self.search_type == 'product':
            queryset = Product.objects.search(self.search_query).order_by('price')
        elif self.search_type == 'product_type':
            initial_queryset = ProductType.objects.search(self.search_query)
            queryset = initial_queryset.product_price_annotation().order_by('views')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.search_type == 'product':
            context['aggregations'] = self.object_list.price_aggregation()
        return context

    def get_pagination_url(self):
        params = self.request.GET.dict().copy()
        params.update({'page': ''})
        return '?' + urlencode(params)
