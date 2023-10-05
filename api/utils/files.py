def bytes_to_mb(bytes_size: int) -> int:
    """
    Converts bytes to megabytes and rounds the
    result down.
    """
    return round(bytes_size / (1024 * 1024))


def mb_to_bytes(mb_size: int | float) -> int:
    """
    Converts megabytes to bytes and rounds the
    result down.
    """
    return round(mb_size * (1024 * 1024))
