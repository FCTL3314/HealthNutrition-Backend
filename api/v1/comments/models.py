from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from api.v1.comments.managers import BaseCommentManager


class Comment(MPTTModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
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

    objects = BaseCommentManager()

    def __str__(self):
        return self.text
