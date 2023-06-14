from django.urls import resolve


def current_url_name(request):
    """
    Returns a name of current url.

    Example:
        'http://127.0.0.1:8000/products/' - 'products:index'
    """
    return {"current_url_name": resolve(request.path).url_name}
