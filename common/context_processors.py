from django.urls import resolve


def current_url_name(request):
    """Returns a pattern name of current url."""
    return {"current_url_name": resolve(request.path).url_name}
