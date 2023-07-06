from django.conf import settings
from django.views.generic import DetailView

from common import mixins as common_views
from interactions.comments.forms import StoreCommentForm
from stores.models import Store


class StoreDetailView(
    common_views.TitleMixin,
    common_views.CommentsMixin,
    common_views.VisitsTrackingMixin,
    DetailView,
):
    model = Store
    form_class = StoreCommentForm
    template_name = "stores/store_detail.html"

    visit_cache_template = settings.STORE_VIEW_TRACKING_CACHE_KEY

    def get_title(self):
        return self.object.name

    @property
    def comments(self):
        return self.object.get_comments()

    def get_visit_cache_template_kwargs(self):
        remote_addr = self.request.META.get("REMOTE_ADDR")
        kwargs = {"addr": remote_addr, "id": self.object.id}
        return kwargs

    def not_visited(self):
        self.object.increase("views")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_products"] = self.object.popular_products()[
            : settings.PRODUCTS_PAGINATE_BY
        ]
        return context
