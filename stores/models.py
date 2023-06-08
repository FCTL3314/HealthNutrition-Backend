from django.db import models
from django.urls import reverse

from common.models import IncrementMixin, SlugifyMixin


class Store(SlugifyMixin, IncrementMixin, models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)
    logo = models.ImageField(upload_to='stores')
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stores:store-detail', args=(self.slug,))

    def popular_products(self):
        return self.product_set.order_by('-views')
