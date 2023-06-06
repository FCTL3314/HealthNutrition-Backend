from django.conf import settings

from common.views import CommonDetailView
from interactions.forms import StoreCommentForm
from stores.models import Store


class StoreDetailView(CommonDetailView):
    model = Store
    form_class = StoreCommentForm
    template_name = 'stores/store_detail.html'

    view_tracking_cache_template = settings.STORE_VIEW_TRACKING_CACHE_KEY

    def get_comments(self):
        return self.object.storecomment_set.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = self.object.popular_products()[:12]
        return context
