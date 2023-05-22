from urllib.parse import urlencode

from django.conf import settings
from django.db.models import Avg, Max, Min
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import ProductType
from utils.common.views import PaginationUrlMixin, TitleMixin


class BaseProductView(TitleMixin, PaginationUrlMixin, FormMixin, ListView):
    form_class = SearchForm
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search_query')
        self.search_type = self.request.GET.get('search_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['search_query'] = self.search_query
        kwargs['search_type'] = self.search_type
        return kwargs

    def get_pagination_url(self):
        if not self.search_query:
            return super().get_pagination_url()
        params = {'search_query': self.search_query, 'search_type': self.search_type, 'page': ''}
        return '?' + urlencode(params)


class ProductTypeView(BaseProductView):
    template_name = 'products/index.html'
    ordering = ('views',)

    def get_queryset(self):
        queryset = ProductType.objects.popular()
        result = ProductType.objects.annotate_products_statistic(queryset)
        return result.order_by(*self.ordering)


class ProductView(BaseProductView):
    model = ProductType
    template_name = 'products/products.html'
    ordering = ('price',)

    def dispatch(self, request, *args, **kwargs):
        product_type_slug = kwargs.get('product_type')
        self.product_type = get_object_or_404(self.model, slug=product_type_slug)
        self.products = self.product_type.product_set.all()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.product_type.increment_views()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.products.prefetch_related('store')
        return queryset.order_by(*self.ordering)

    def get_title(self):
        return self.product_type.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_price_stats = self.products.aggregate(
            min_price=Round(Min('price'), settings.PRICE_ROUNDING),
            max_price=Round(Max('price'), settings.PRICE_ROUNDING),
            avg_price=Round(Avg('price'), settings.PRICE_ROUNDING),
        )
        context.update(products_price_stats)
        return context
