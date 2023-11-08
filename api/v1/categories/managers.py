from django.db import models


class CategoryQuerySet(models.QuerySet):
    ...


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    ...
