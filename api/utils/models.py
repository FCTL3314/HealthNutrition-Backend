from django.db.models import Model


def invalidate_prefetch_cache(instance: Model) -> None:
    """
    Invalidates object cache created by prefetch related
    method.

    If 'prefetch_related' has been applied to a queryset,
    we need to forcibly invalidate the prefetch cache on
    the instance.
    """
    if getattr(instance, "_prefetched_objects_cache", None):
        instance._prefetched_objects_cache = {}
