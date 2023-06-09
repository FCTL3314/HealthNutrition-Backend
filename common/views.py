from abc import ABC, abstractmethod

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin


class TitleMixin:
    """Allows to create and add a title variable to the contest."""

    title = None
    context_title_name = 'title'

    def get_title(self) -> str:
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
    """Allows to create and add a pagination_url variable to the context."""

    context_pagination_url_name = 'pagination_url'

    def get_pagination_url(self) -> str:
        return '?page='

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_pagination_url_name] = self.get_pagination_url()
        return context


class BaseVisitsTrackingMixin(ABC):
    """
    Checks if any object, for example, the user has visited this view,
    and implements interfaces to determine the logic if the view was
    visited or not visited by object.

    The object can be either a user, which will be most often, or any
    other entity for which a unique cache key can be created.
    """
    _visit_cache_key = None
    _visit_cache_time = None

    @property
    @abstractmethod
    def visit_cache_key(self) -> str:
        """
        The unique cache key for the object visiting this view.

        Example:
            'user_addr:127.0.0.1_product_id:4'
            That is, a user with ip 127.0.0.1 visited the product object with id 4.
        """
        return self._visit_cache_key

    @visit_cache_key.setter
    def visit_cache_key(self, value):
        self._visit_cache_key = value

    @property
    @abstractmethod
    def visit_cache_time(self) -> int:
        """The time that the cache(object visit) will be stored."""
        return self._visit_cache_time

    @visit_cache_time.setter
    def visit_cache_time(self, value):
        self._visit_cache_time = value

    def _has_visited(self) -> bool:
        """Checks if the object has visited this view, that is, if its cache exists."""
        is_exists = cache.get(self.visit_cache_key)
        return bool(is_exists)

    def visited(self) -> None:
        """The logic if the view has been visited by an object before."""
        pass

    def not_visited(self) -> None:
        """The logic if the view has not been visited by an object before."""
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
    @abstractmethod
    def visit_cache_template(self) -> str:
        """
        Allows to use template strings to create a cache key.

        Example:
            return 'addr:{addr:}_product:{id:}'
        """
        return self._visit_cache_template

    @visit_cache_template.setter
    def visit_cache_template(self, value):
        self._visit_cache_template = value

    @abstractmethod
    def get_visit_cache_template_kwargs(self) -> dict:
        """
        Keyword arguments that will be passed to the .format() method when
        creating a template cache string.

        Example:
            kwargs = {'addr': '127.0.0.1', 'id': '4'}
            return kwargs
        """
        pass

    @property
    def visit_cache_key(self) -> str:
        key = self.visit_cache_template
        kwargs = self.get_visit_cache_template_kwargs()
        return key.format(**kwargs)


class CommentsMixin(FormMixin, ABC):
    _comments = None

    @property
    @abstractmethod
    def comments(self) -> QuerySet:
        """Returns a QuerySet of comment objects."""
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
