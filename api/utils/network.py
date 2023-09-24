def get_client_address(request):
    if x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR") is not None:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")
