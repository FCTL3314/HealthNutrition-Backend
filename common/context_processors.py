from django.urls import resolve


def current_url_name(request):
    return {'current_url_name': resolve(request.path).url_name}
