import os

from django.conf import settings


def get_static_file(path: str) -> str:
    """Join the static files directory with the path to the static file."""
    return os.path.join(settings.STATIC_URL, path)
