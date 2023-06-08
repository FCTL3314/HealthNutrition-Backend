from abc import ABC, abstractmethod

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

from common.models import increment_views
from utils.validators import validate_attribute_not_none


class TitleMixin:
    """Allows to add the title variable to the context."""

    title = None
    context_title_name = 'title'

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context[self.context_title_name] = f'{title} | StoreTracker' if title else 'StoreTracker'
        return context


class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class PaginationUrlMixin:
    """Allows to create pagination url and pass it to the context."""

    context_pagination_url_name = 'pagination_url'

    def get_pagination_url(self):
        return '?page='

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_pagination_url_name] = self.get_pagination_url()
        return context


class BaseVisitsTrackingMixin(ABC):
    """Checks if this view has been called based on whether the given cache exists."""
    _visit_cache_key = None
    _visit_cache_time = None

    @property
    def visit_cache_key(self):
        """
        The cache key with which in the future it will be possible to determine
        whether this entity has watched this view.
        """
        validate_attribute_not_none(self._visit_cache_key, 'visit_cache_key')
        return self._visit_cache_key

    @visit_cache_key.setter
    def visit_cache_key(self, value):
        self._visit_cache_key = value

    @property
    def visit_cache_time(self):
        """The time that the cache will be stored."""
        validate_attribute_not_none(self._visit_cache_time, 'visit_cache_time')
        return self._visit_cache_time

    @visit_cache_time.setter
    def visit_cache_time(self, value):
        self._visit_cache_time = value

    def _has_visited(self):
        """Checks if the cache exists."""
        is_exists = cache.get(self.visit_cache_key)
        return bool(is_exists)

    def visited(self):
        """Logic if the cache exists."""
        pass

    def not_visited(self):
        """Logic if the cache not exists."""
        pass

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self._has_visited():
            self.visited()
        else:
            cache.set(self.visit_cache_key, True, self.visit_cache_time)
            self.not_visited()
        return response


class VisitsTrackingMixin(BaseVisitsTrackingMixin):
    _visit_cache_template = None
    visit_cache_time = settings.VISITS_CACHE_TIME

    @property
    def visit_cache_template(self):
        validate_attribute_not_none(self._visit_cache_template, 'visit_cache_template')
        return self._visit_cache_template

    @visit_cache_template.setter
    def visit_cache_template(self, value):
        self._visit_cache_template = value

    @abstractmethod
    def get_visit_cache_template_kwargs(self):
        pass

    @property
    def visit_cache_key(self):
        key = self.visit_cache_template
        kwargs = self.get_visit_cache_template_kwargs()
        return key.format(**kwargs)


class SingleObjectVisitsTrackingMixin(VisitsTrackingMixin):

    def not_visited(self):
        increment_views(self.object)

    def get_visit_cache_template_kwargs(self):
        remote_addr = self.request.META.get('REMOTE_ADDR')
        kwargs = {'addr': remote_addr, 'id': self.object.id}
        return kwargs


class CommentsMixin(FormMixin, ABC):
    _comments = None

    @property
    def comments(self):
        validate_attribute_not_none(self._comments, 'comments')
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments = value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = self.comments.prefetch_related('author')
        comments_count = comments.count()

        context['comments'] = comments[:settings.COMMENTS_PAGINATE_BY]
        context['comments_count'] = comments_count
        context['has_more_comments'] = comments_count > settings.COMMENTS_PAGINATE_BY
        return context
