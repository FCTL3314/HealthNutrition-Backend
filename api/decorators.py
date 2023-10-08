from functools import wraps

from django.db.models import QuerySet


def order_queryset(*ordering: str):
    """
    Order the queryset returned by the function using
    the ordering parameter.
    """

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs) -> QuerySet:
            queryset = func(*args, **kwargs)
            return queryset.order_by(*ordering)

        return inner

    return outer
