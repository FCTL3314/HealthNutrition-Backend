def get_referer_or_default(request, default='/'):
    referer = request.META.get('HTTP_REFERER')
    return referer if referer else default
