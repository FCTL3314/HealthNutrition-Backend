from django.template.defaulttags import register

from django.conf import settings


@register.filter()
def subtract(value, arg):
    return round(value - arg, settings.PRICE_ROUNDING)
