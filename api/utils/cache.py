from typing import Any, Callable

from django.core.cache import cache


def get_cached_data_or_set_new(key: str, callback: Callable, timeout: int) -> Any:
    """
    Checks if the cache exists for the given key. If not present,
    it caches the data obtained from calling the callback function
    for timeout seconds.
    """
    data = cache.get(key)
    if data is None:
        data = callback()
        cache.set(key, data, timeout)
    return data
