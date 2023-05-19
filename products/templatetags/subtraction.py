from django.conf import settings
from django.template.defaulttags import register


@register.filter()
def subtract(value, arg):
    return round(value - arg, settings.PRICE_ROUNDING)
