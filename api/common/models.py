from django.db import models


class BaseViewsModel(models.Model):
    views = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
