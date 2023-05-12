from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(to='stores.Store', on_delete=models.CASCADE)
    product_type = models.ForeignKey(to='products.ProductType', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.store}'


class ProductType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='products/product_types')

    def __str__(self):
        return self.name
