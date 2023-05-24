import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    slug = models.SlugField(unique=True)
    comparisons = models.ManyToManyField('products.Product', through='comparisons.Comparison', blank=True)

    def get_image_url(self):
        return self.image.url if self.image else os.path.join(settings.STATIC_URL, 'images/default_user_image.png')

    def update_slug(self):
        self.slug = slugify(self.username)

    def __str__(self):
        return self.username
