from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)
    logo = models.ImageField(upload_to='stores')
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
