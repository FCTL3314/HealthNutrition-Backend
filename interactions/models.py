from django.db import models


class AbstractComment(models.Model):
    author = models.ForeignKey(to='users.User', null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=516)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class ProductComment(AbstractComment):
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)


class StoreComment(AbstractComment):
    store = models.ForeignKey(to='stores.Store', on_delete=models.CASCADE)
