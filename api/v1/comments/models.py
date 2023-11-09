from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from api.v1.comments.managers import BaseCommentManager
from api.v1.products.models import Product


class Comment(MPTTModel):
    text = models.CharField(max_length=516)
    author = models.ForeignKey(to="users.User", null=True, on_delete=models.CASCADE)
    parent = TreeForeignKey(
        to="self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")
    object_id = models.PositiveIntegerField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    ALLOWED_CONTENT_TYPE_MODEL_NAMES = {
        Product._meta.model_name,
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
