from django.db import models


class ProductTypeManager(models.Manager):

    def popular(self):
        return self.order_by('-views')
