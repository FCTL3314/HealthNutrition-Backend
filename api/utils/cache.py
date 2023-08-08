from typing import Any, Callable

from django.core.cache import cache


def get_cached_data_or_set_new(key: str, callback: Callable, timeout: int) -> Any:
    """
    Returns the cached data if it exists, otherwise calls the
    callback function to get and cache the data.
    """
    data = cache.get(key)
    if data is None:
        data = callback()
        cache.set(key, data, timeout)
    return data
