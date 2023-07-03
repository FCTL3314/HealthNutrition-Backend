from functools import wraps


def order_queryset(*ordering):
    """
    Sorts the queryset returned by the function using the ordering parameter.
    """

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            queryset = func(*args, **kwargs)
            return queryset.order_by(*ordering)

        return wrapper

    return outer
