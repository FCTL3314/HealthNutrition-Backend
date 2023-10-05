from django.db import models


class ViewsModelMixin(models.Model):
    views = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
