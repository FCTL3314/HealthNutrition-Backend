def get_referer_or_default(request, default: str | None = "/") -> str:
    """
    Returns the url from which the user went to this page,
    if there is no such url, then returns default argument.
    """
    referer = request.META.get("HTTP_REFERER")
    return referer if referer else default
