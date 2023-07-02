from functools import wraps


def order_queryset(*ordering):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            queryset = func(*args, **kwargs)
            return queryset.order_by(*ordering)

        return wrapper

    return outer
