from django.views.generic.detail import DetailView

from common.views import TitleMixin
from stores.models import Store


class StoreDetailView(TitleMixin, DetailView):
    model = Store
    slug_url_kwarg = 'store_slug'
    template_name = 'stores/stores.html'

    def get_title(self):
        return self.object.name
