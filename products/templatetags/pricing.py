from django.conf import settings
from django.template.defaulttags import register


@register.filter()
def price_subtract(value, arg):
    return round(value - arg, settings.PRICE_ROUNDING)
