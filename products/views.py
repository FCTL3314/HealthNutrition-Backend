from django.conf import settings
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView

from common.views import (CommentsMixin, CommonListView, SearchMixin,
                          TitleMixin, VisitsTrackingMixin)
from interactions.forms import ProductCommentForm
from products.models import Product, ProductType


class ProductTypeListView(SearchMixin, TitleMixin, CommonListView):
    ordering = settings.PRODUCT_TYPES_ORDERING
    paginate_by = settings.PRODUCT_TYPES_PAGINATE_BY
    template_name = 'products/product_types.html'
    title = 'Categories'
    object_list_title = 'Discover Popular Product Categories'
    object_list_description = 'Explore our curated list of popular product categories, sorted by their popularity ' \
                              'among users.'

    def get_queryset(self):
        initial_queryset = ProductType.objects.popular()
        queryset = initial_queryset.product_price_annotation()
        return queryset.order_by(*self.ordering)


class ProductListView(VisitsTrackingMixin, SearchMixin, TitleMixin, CommonListView):
    model = ProductType
    ordering = settings.PRODUCTS_ORDERING
    paginate_by = settings.PRODUCTS_PAGINATE_BY
    template_name = 'products/products.html'
    object_list_description = 'Discover a wide range of products available in the selected category.'
    visit_cache_template = settings.PRODUCT_TYPE_VIEW_TRACKING_CACHE_TEMPLATE

    product_type: ProductType

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        self.product_type = get_object_or_404(self.model, slug=slug)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.product_type.get_products_with_stores()
        return queryset.order_by(*self.ordering)

    def get_visit_cache_template_kwargs(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        kwargs = {'addr': remote_addr, 'id': self.product_type.id}
        return kwargs

    def not_visited(self):
        self.product_type.increase('views')

    def get_title(self):
        return self.product_type.name

    def get_object_list_title(self):
        return f'Products in the category "{self.product_type.name}"'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context


class ProductDetailView(CommentsMixin, VisitsTrackingMixin, TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    form_class = ProductCommentForm
    visit_cache_template = settings.PRODUCT_VIEW_TRACKING_CACHE_TEMPLATE

    def get_title(self):
        return self.object.name

    @property
    def comments(self):
        return self.object.get_comments()

    def get_visit_cache_template_kwargs(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        kwargs = {'addr': remote_addr, 'id': self.object.id}
        return kwargs

    def not_visited(self):
        self.object.increase('views')


class SearchRedirectView(SearchMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        match self.search_type:
            case 'product':
                redirect_url = reverse('products:product-search')
            case 'product_type':
                redirect_url = reverse('products:product-type-search')
            case _:
                raise BadRequest('search_type not in product or product_type')

        params = self.request.META.get('QUERY_STRING')
        return f'{redirect_url}?{params}'


class BaseSearchView(SearchMixin, TitleMixin, CommonListView):
    object_list_title = 'Search Results'
    object_list_description = 'Explore the results of your search query.'


class ProductTypeSearchListView(BaseSearchView):
    ordering = settings.PRODUCT_TYPES_ORDERING
    paginate_by = settings.PRODUCT_TYPES_PAGINATE_BY
    template_name = 'products/product_types.html'
    title = 'Category Search'

    def get_queryset(self):
        queryset = ProductType.objects.search(self.search_query)
        queryset = queryset.product_price_annotation().order_by(*self.ordering)
        return queryset


class ProductSearchListView(BaseSearchView):
    ordering = settings.PRODUCTS_ORDERING
    paginate_by = settings.PRODUCTS_PAGINATE_BY
    template_name = 'products/products.html'
    title = 'Product Search'

    def get_queryset(self):
        return Product.objects.search(self.search_query).order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context
