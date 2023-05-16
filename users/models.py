from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users', default='users/default_user_image.png', null=True, blank=True)
    slug = models.SlugField(unique=True)
    comparisons = models.ManyToManyField('products.Product', through='comparisons.Comparison', blank=True)

    def update_slug(self):
        self.slug = slugify(self.username)

    def __str__(self):
        return self.username
