from django.conf import settings
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from common.mixins import TitleMixin, UserViewTrackingMixin
from interactions.forms import StoreCommentForm
from stores.models import Store


class StoreDetailView(TitleMixin, UserViewTrackingMixin, FormMixin, DetailView):
    model = Store
    form_class = StoreCommentForm
    template_name = 'stores/store_detail.html'

    view_tracking_cache_time = 60 * 30

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

        comments = self.object.storecomment_set.order_by('-created_at')
        comments_count = comments.count()

        context['comments'] = comments[:settings.COMMENTS_PAGINATE_BY]
        context['comments_count'] = comments_count
        context['has_more_comments'] = comments_count > settings.COMMENTS_PAGINATE_BY
        return context
