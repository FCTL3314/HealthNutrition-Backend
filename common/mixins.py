from abc import abstractmethod, ABC

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect


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


class UserViewTrackingMixin(ABC):
    """Tracking of whether the user called a view during a some time."""

    @property
    @abstractmethod
    def view_tracking_cache_key(self):
        pass

    @property
    @abstractmethod
    def view_tracking_cache_time(self):
        """The time that a user's view is stored in the cache."""
        pass

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self._has_viewed():
            self.user_viewed()
        else:
            cache.set(self.view_tracking_cache_key, True, self.view_tracking_cache_time)
            self.user_not_viewed()
        return response

    def user_viewed(self):
        """Logic if the user has already called this view."""
        pass

    def user_not_viewed(self):
        """Logic if the user has not yet called this view."""
        pass

    def _has_viewed(self):
        """Checks if the cache of the user who called the view exists."""
        is_exists = cache.get(self.view_tracking_cache_key)
        return bool(is_exists)
