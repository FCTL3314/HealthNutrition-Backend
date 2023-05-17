from django.template.defaulttags import register


@register.filter()
def subtract(value, arg):
    return round(value - arg, 2)
