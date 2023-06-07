from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from common.mixins import PaginationUrlMixin, TitleMixin, UserViewTrackingMixin
from common.views import CommonDetailView
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
        context.update(self.object_list.price_aggregation())
        return context


class ProductDetailView(CommonDetailView):
    model = Product
    form_class = ProductCommentForm
    template_name = 'products/product_detail.html'

    view_tracking_cache_template = settings.PRODUCT_VIEW_TRACKING_CACHE_KEY

    def get_comments(self):
        return self.object.productcomment_set.order_by('-created_at')


class SearchRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        search_type = self.request.GET.get('search_type')

        match search_type:
            case 'product':
                redirect_url = reverse('products:product-search')
            case 'product_type':
                redirect_url = reverse('products:product-type-search')
            case _:
                raise BadRequest('search_type not in product or product_type')

        params = self.request.META.get('QUERY_STRING')
        return f'{redirect_url}?{params}'


class BaseSearchView(BaseProductsView):
    object_list_title = 'Search Results'
    object_list_description = 'Explore the results of your search query.'

    def get_pagination_url(self):
        params = self.request.GET.dict().copy()
        params['page'] = ''
        return '?' + urlencode(params)


class ProductSearchListView(BaseSearchView):
    title = 'Product Search'

    def get_queryset(self):
        return Product.objects.search(self.search_query).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.price_aggregation())
        return context


class ProductTypeSearchListView(BaseSearchView):
    title = 'Category Search'

    def get_queryset(self):
        queryset = ProductType.objects.search(self.search_query)
        queryset = queryset.product_price_annotation().order_by('views')
        return queryset

    def get_pagination_url(self):
        params = self.request.GET.dict().copy()
        params.update({'page': ''})
        return '?' + urlencode(params)
