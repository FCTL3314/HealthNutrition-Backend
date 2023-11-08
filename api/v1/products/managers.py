from django.db import models


class ProductQuerySet(models.QuerySet):
    ...


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    ...
