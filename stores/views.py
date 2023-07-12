from django.conf import settings
from django.views.generic import DetailView

from common import mixins as common_views
from interactions.comments.forms import StoreCommentForm
from stores.models import Store


class StoreDetailView(
    common_views.TitleMixin,
    common_views.CommentsMixin,
    common_views.CachedUserVisitsTrackingMixin,
    DetailView,
):
    model = Store
    form_class = StoreCommentForm
    template_name = "stores/store_detail.html"

    def get_title(self):
        return self.object.name

    @property
    def comments(self):
        return self.object.get_comments()

    @property
    def visit_cache_identifier(self) -> str:
        remote_addr = self.request.META.get("REMOTE_ADDR")
        kwargs = {"addr": remote_addr, "id": self.object.id}
        return settings.STORE_VISIT_CACHE_TEMPLATE.format(**kwargs)

    def user_not_visited(self):
        self.object.increase("views")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_products = self.object.popular_products()
        context["popular_products"] = popular_products[:settings.PRODUCTS_PAGINATE_BY]
        return context
