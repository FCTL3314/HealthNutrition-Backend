from django.views.generic.list import ListView

from products.models import ProductType
from utils.common.views import TitleMixin


class IndexListView(TitleMixin, ListView):
    model = ProductType
    title = 'StoreTracker'
    template_name = 'index.html'
