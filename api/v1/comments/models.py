from django.db import models
from django.urls import reverse

from api.v1.comments.managers import BaseCommentManager


class BaseComment(models.Model):
    author = models.ForeignKey(to="users.User", null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=516)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    objects = BaseCommentManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class ProductComment(BaseComment):
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:comments:product-detail", args=(self.id,))


class StoreComment(BaseComment):
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:comments:store-detail", args=(self.id,))
