from django.conf import settings
from django.views.generic import DetailView

from common.mixins import (CommentsMixin, SingleObjectVisitsTrackingMixin,
                           TitleMixin)
from interactions.forms import StoreCommentForm
from stores.models import Store


class StoreDetailView(TitleMixin, CommentsMixin, SingleObjectVisitsTrackingMixin, DetailView):
    model = Store
    form_class = StoreCommentForm
    template_name = 'stores/store_detail.html'

    visit_cache_template = settings.STORE_VIEW_TRACKING_CACHE_KEY

    def get_title(self):
        return self.object.name

    @property
    def comments(self):
        return self.object.storecomment_set.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = self.object.popular_products()[:12]
        return context
