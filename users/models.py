from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.username
