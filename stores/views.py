from django.conf import settings
from django.views.generic.detail import DetailView

from common.views import TitleMixin, UserViewTrackingMixin
from stores.models import Store


class StoreDetailView(TitleMixin, UserViewTrackingMixin, DetailView):
    model = Store
    slug_url_kwarg = 'store_slug'
    template_name = 'stores/stores.html'

    view_tracking_cache_time = settings.STORE_VIEW_TRACKING_CACHE_TIME

    def get_view_tracking_cache_key(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return settings.STORE_VIEW_TRACKING_CACHE_KEY.format(addr=remote_addr, id=self.object.id)

    def user_not_viewed(self):
        self.object.increment_views()

    def get_title(self):
        return self.object.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = self.object.popular_products()[:12]
        return context
