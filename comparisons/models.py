from django.db import models

from comparisons.managers import ComparisonManager


class Comparison(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)

    objects = ComparisonManager()

    def __str__(self):
        return f'{self.user.username} | {self.product.name}'
