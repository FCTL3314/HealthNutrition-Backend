from django.db import models


class BaseComment(models.Model):
    author = models.ForeignKey(to="users.User", null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=516)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class ProductComment(BaseComment):
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)


class StoreComment(BaseComment):
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)
