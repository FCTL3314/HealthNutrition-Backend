from abc import ABC, abstractmethod
from functools import cached_property
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

from products.forms import SearchForm


class TitleMixin:
    """Mixin to create and add a title variable to the context."""

    title: str = None
    context_title_name: str = "title"

    def get_title(self) -> str:
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context[self.context_title_name] = (
            f"{title} | StoreTracker" if title else "StoreTracker"
        )
        return context


class PaginationUrlMixin:
    """Mixin to create and add a pagination_url variable to the context."""

    context_pagination_url_name: str = "pagination_url"

    def get_pagination_url(self) -> str:
        params = self.request.GET.dict().copy()
        if "page" in params:
            params.pop("page")
        encoded_params = urlencode(params)
        return f"?{encoded_params}&page=" if encoded_params else "?page="

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_pagination_url_name] = self.get_pagination_url()
        return context


class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REQUIRED_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class BaseVisitsTrackingMixin(ABC):
    """
    Mixin that checks if user (not necessarily a user, can be any object), has visited
    this view, implements interfaces to determine the logic if the view
    was visited or not visited by user.
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
    def visit_cache_time(self) -> int:
        """The time that the cache(object visit) will be stored."""
        return settings.VISITS_CACHE_TIME

    def _has_visited(self) -> bool:
        """Checks if the user has visited this view, i.e. if its cache exists."""
        return bool(cache.get(self.visit_cache_key))

    def visited(self) -> None:
        """The logic if the view has been visited by a user before."""
        pass

    def not_visited(self) -> None:
        """The logic if the view has not been visited by a user before."""
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
    """
    Wrapper for BaseVisitsTrackingMixin to use cache_template
    instead of regular cache_key.
    """

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
            return {'addr': '127.0.0.1', 'id': '4'}
        """
        pass

    @property
    def visit_cache_key(self) -> str:
        key = self.visit_cache_template
        kwargs = self.get_visit_cache_template_kwargs()
        return key.format(**kwargs)


class SearchFormMixin(FormMixin):
    """A mixin for finding and storing the search query and search type."""

    form_class = SearchForm

    def dispatch(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get("search_query", "")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Passes the search query and search type to the form initialization
        so that the form will then set them as initial for its fields.
        """
        kwargs = super().get_form_kwargs()
        kwargs["search_query"] = self.search_query
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        return context


class SearchWithSearchTypeFormMixin(SearchFormMixin):
    """A wrapper for SearchMixin that adds a search type."""

    form_class = SearchForm

    def dispatch(self, request, *args, **kwargs):
        self.search_type = self.request.GET.get("search_type")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["search_type"] = self.search_type
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_type"] = self.search_type
        return context


class CommentsMixin(FormMixin, ABC):
    """Mixin that provides comments and additional comments info for the context."""

    @property
    @abstractmethod
    def comments(self) -> QuerySet:
        pass

    @cached_property
    def comments_count(self) -> int:
        return self.comments.count()

    def has_more_comments(self) -> bool:
        return self.comments_count > settings.COMMENTS_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        prefetched_comments = self.comments.prefetch_related("author")

        context["comments"] = prefetched_comments[: settings.COMMENTS_PAGINATE_BY]
        context["comments_count"] = self.comments_count
        context["has_more_comments"] = self.has_more_comments()
        return context


class ObjectListInfoMixin:
    """Mixin that provides object list title and description for the context."""

    _object_list_title: str = ""
    _object_list_description: str = ""

    @property
    def object_list_title(self) -> str:
        return self._object_list_title

    @property
    def object_list_description(self) -> str:
        return self._object_list_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list_title"] = self.object_list_title
        context["object_list_description"] = self.object_list_description
        return context
