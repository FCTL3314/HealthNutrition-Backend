from django.db import models


class Comparison(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)
