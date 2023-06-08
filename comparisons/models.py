from django.db import models


class Comparison(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.product.name}'
