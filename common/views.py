from abc import ABC, abstractmethod
from functools import cached_property
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from products.forms import SearchForm


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


class PaginationUrlMixin:
    """Allows to create and add a pagination_url variable to the context."""

    context_pagination_url_name = 'pagination_url'

    def get_pagination_url(self) -> str:
        params = self.request.GET.dict().copy()
        if 'page' in params:
            params.pop('page')
        encoded_params = urlencode(params)
        return f'?{encoded_params}&page=' if encoded_params else '?page='

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_pagination_url_name] = self.get_pagination_url()
        return context


class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class BaseVisitsTrackingMixin(ABC):
    """
    Checks if any object, for example, the user has visited this view,
    and implements interfaces to determine the logic if the view was
    visited or not visited by object.

    The object can be either a user, which will be most often, or any
    other entity for which a unique cache key can be created.
    """

    @property
    @abstractmethod
    def visit_cache_key(self) -> str:
        """
        The unique cache key for the object visiting this view.

        Example:
            'user_addr:127.0.0.1_product_id:4'
            That is, a user with ip 127.0.0.1 visited the product object with id 4.
        """
        pass

    @property
    @abstractmethod
    def visit_cache_time(self) -> int:
        """The time that the cache(object visit) will be stored."""
        pass

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
    visit_cache_time = settings.VISITS_CACHE_TIME

    @property
    @abstractmethod
    def visit_cache_template(self) -> str:
        """
        Allows to use template strings to create a cache key.

        Example:
            return 'addr:{addr:}_product:{id:}'
        """
        pass

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


class SearchMixin(FormMixin):
    form_class = SearchForm

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('search_query', '')
        self.search_type = self.request.GET.get('search_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['search_query'] = self.search_query
        kwargs['search_type'] = self.search_type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.search_query
        context['search_type'] = self.search_type
        return context


class CommentsMixin(FormMixin, ABC):
    """
        Mixin that provides comments and additional comments info for the context.

        Attributes:
            _comments (QuerySet): QuerySet of comments for any object.
    """
    _comments: QuerySet = None

    @property
    @abstractmethod
    def comments(self) -> QuerySet:
        return self._comments

    @cached_property
    def comments_count(self):
        return self.comments.count()

    def has_more_comments(self):
        return self.comments_count > settings.COMMENTS_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        prefetched_comments = self.comments.prefetch_related('author')

        context['comments'] = prefetched_comments[:settings.COMMENTS_PAGINATE_BY]
        context['comments_count'] = self.comments_count
        context['has_more_comments'] = self.has_more_comments()
        return context


class ObjectListInfoMixin:
    """
        Mixin that provides object list title and description for the context.

        Attributes:
            _object_list_title (str): Title for the object list.
            _object_list_description (str): Description for the object list.
    """
    _object_list_title: str = ''
    _object_list_description: str = ''

    @property
    def object_list_title(self) -> str:
        return self._object_list_title

    @property
    def object_list_description(self) -> str:
        return self._object_list_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list_title'] = self.object_list_title
        context['object_list_description'] = self.object_list_description
        return context


class CommonListView(PaginationUrlMixin, TitleMixin, ObjectListInfoMixin, ListView):
    pass
