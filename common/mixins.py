from abc import ABC, abstractmethod
from functools import cached_property
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin


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
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class BaseUserVisitsTrackingMixin(ABC):
    """
    Mixin that tracks if user, has visited this view, implements interfaces
    to determine the logic if the view was visited or not visited by user.
    """

    @property
    def visit_storage_time(self) -> int:
        """The time that user's visit will be stored."""
        return settings.VISITS_CACHE_TIME

    @abstractmethod
    def _has_visited(self) -> bool:
        """
        Returns True or False based on whether the user visited
        this view before
        """
        pass

    def user_visited(self) -> None:
        """The logic if the view has been visited by a user before."""
        pass

    def user_not_visited(self) -> None:
        """The logic if the view has not been visited by a user before."""
        pass

    @abstractmethod
    def _save_user_visit(self) -> None:
        """A way to save the user's visit."""
        pass

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self._has_visited():
            self.user_visited()
        else:
            self._save_user_visit()
            self.user_not_visited()
        return response


class CachedUserVisitsTrackingMixin(BaseUserVisitsTrackingMixin):

    @property
    @abstractmethod
    def visit_cache_identifier(self) -> str:
        """
        The unique cache key for the object visiting this view.

        Example:
            'user_addr:127.0.0.1_product_id:4'
            A user with ip 127.0.0.1 visited the product object with id 4.
        """
        pass

    def _has_visited(self) -> bool:
        """
        Returns True if user visit cache exists, otherwise False.
        """
        return bool(cache.get(self.visit_cache_identifier))

    def _save_user_visit(self) -> None:
        """Saves user visit to the cache."""
        cache.set(self.visit_cache_identifier, True, self.visit_storage_time)

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self._has_visited():
            self.user_visited()
        else:
            self._save_user_visit()
            self.user_not_visited()
        return response


class CommentsMixin(FormMixin, ABC):
    """
    Mixin that provides comments and additional comments info for the context.
    """

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
