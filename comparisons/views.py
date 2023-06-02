from django.views.generic import ListView

from common.mixins import TitleMixin
from products.models import ProductType


class ComparisonProductTypeListView(TitleMixin, ListView):
    model = ProductType
    title = 'Comparisons'
    template_name = 'comparisons/comparison.html'

    def get_queryset(self):
        products = self.request.user.comparison_set.all()
        product_types_id = products.values_list('product__product_type', flat=True)
        product_types = self.model.objects.filter(id__in=product_types_id)
        return product_types.product_price_annotation()
