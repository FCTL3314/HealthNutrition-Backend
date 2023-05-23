from urllib.parse import urlencode

from django.conf import settings
from django.db.models import Avg, Max, Min, Q
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import Product, ProductType
from utils.common.views import PaginationUrlMixin, TitleMixin


class BaseProductsView(TitleMixin, PaginationUrlMixin, FormMixin, ListView):
    form_class = SearchForm
    paginate_by = 12
    objects_title = ''
    objects_description = ''

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search_query')
        self.search_type = self.request.GET.get('search_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['search_query'] = self.search_query
        kwargs['search_type'] = self.search_type
        return kwargs

    def get_objects_title(self):
        return self.objects_title

    def get_objects_description(self):
        return self.objects_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects_title'] = self.get_objects_title()
        context['objects_description'] = self.get_objects_description()
        return context

    def get_pagination_url(self):
        if self.search_query:
            return f'?' + urlencode({'search_query': self.search_query, 'search_type': self.search_type, 'page': ''})
        return super().get_pagination_url()


class ProductTypeListView(BaseProductsView):
    template_name = 'products/index.html'
    ordering = ('views',)
    title = 'Categories'

    def get_objects_title(self):
        if self.search_query:
            return 'Searched Categories'
        return 'Featured Categories'

    def get_objects_description(self):
        if self.search_query:
            return 'Categories based on your search, sorted by popularity.'
        return 'Categories of products that users open most often.'

    def get_queryset(self):
        if self.search_query:
            queryset = ProductType.objects.filter(
                Q(name__icontains=self.search_query) | Q(description__icontains=self.search_query),
            )
        else:
            queryset = ProductType.objects.popular()
        result = queryset.annotate_products_statistic()
        return result.order_by(*self.ordering)


class BaseProductListView(BaseProductsView):
    model = ProductType
    template_name = 'products/products.html'
    ordering = ('price',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_price_aggregation = self.object_list.aggregate(
            min_price=Round(Min('price'), settings.PRICE_ROUNDING),
            max_price=Round(Max('price'), settings.PRICE_ROUNDING),
            avg_price=Round(Avg('price'), settings.PRICE_ROUNDING),
        )
        context.update(products_price_aggregation)
        return context


class ProductTypeProductsListView(BaseProductListView):
    objects_description = 'List of products based on the category you selected, sorted by price'

    def dispatch(self, request, *args, **kwargs):
        product_type_slug = kwargs.get('slug')
        self.product_type = get_object_or_404(self.model, slug=product_type_slug)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.product_type.increment_views()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        products = self.product_type.product_set.all()
        queryset = products.prefetch_related('store')
        return queryset.order_by(*self.ordering)

    def get_title(self):
        return self.product_type.name

    def get_objects_title(self):
        return f'Products of category {self.product_type.name}'


class ProductsListView(BaseProductListView):
    title = 'Products'

    def get_queryset(self):
        if self.search_query:
            queryset = Product.objects.filter(
                Q(name__icontains=self.search_query) | Q(card_description__icontains=self.search_query),
            )
        else:
            queryset = Product.objects.all()
        result = queryset.prefetch_related('store')
        return result.order_by(*self.ordering)

    def get_objects_title(self):
        if self.search_query:
            return 'Searched Products'
        return 'List of all products'

    def get_objects_description(self):
        if self.search_query:
            return 'Products based on your search, sorted by popularity.'
        return 'List of all site products sorted by price.'


class SearchRedirectView(View):
    def get(self, request, *args, **kwargs):
        search_query = self.request.GET.get('search_query')
        search_type = self.request.GET.get('search_type')

        query = '?' + urlencode({'search_query': search_query})

        if search_type == 'product':
            return redirect(reverse('products:products') + query)
        elif search_type == 'product_type':
            return redirect(reverse('products:product-types') + query)
        else:
            return redirect('products:products')
