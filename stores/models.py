from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)
    logo = models.ImageField(upload_to='stores')
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def popular_products(self):
        return self.product_set.order_by('-views')

    def increment_views(self):
        self.views += 1
        self.save(update_fields=('views',))
