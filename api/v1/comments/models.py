from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from api.v1.comments.managers import BaseCommentManager
from api.v1.products.models import Product
from api.v1.stores.models import Store


class Comment(MPTTModel):
    author = models.ForeignKey(to="users.User", null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=516)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent = TreeForeignKey(
        to="self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    ALLOWED_CONTENT_TYPE_MODEL_NAMES = {
        Product._meta.model_name,
        Store._meta.model_name,
    }
    ALLOWED_CONTENT_TYPES_QUERYSET = ContentType.objects.filter(
        model__in=ALLOWED_CONTENT_TYPE_MODEL_NAMES
    )

    objects = BaseCommentManager()

    class MPTTMeta:
        order_insertion_by = ("-created_at",)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("api:v1:comments:comments-detail", kwargs={"pk": self.pk})
