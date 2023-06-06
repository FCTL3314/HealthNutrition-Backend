from abc import abstractmethod

from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from common.mixins import TitleMixin, UserViewTrackingMixin


class CustomBaseDetailView(TitleMixin, UserViewTrackingMixin, FormMixin, DetailView):
    view_tracking_cache_template: str
    view_tracking_cache_time = 60 * 30

    def get_view_tracking_cache_key(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return self.view_tracking_cache_template.format(addr=remote_addr, id=self.object.id)

    @abstractmethod
    def get_comments(self):
        pass

    def user_not_viewed(self):
        self.object.increment_views()

    def get_title(self):
        return self.object.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = self.get_comments()
        comments_count = comments.count()

        context['comments'] = comments[:settings.COMMENTS_PAGINATE_BY]
        context['comments_count'] = comments_count
        context['has_more_comments'] = comments_count > settings.COMMENTS_PAGINATE_BY
        return context
