from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from products.forms import SearchForm
from products.models import ProductType
from utils.common.views import TitleMixin


class IndexListView(TitleMixin, FormMixin, ListView):
    model = ProductType
    form_class = SearchForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super().get(request)
