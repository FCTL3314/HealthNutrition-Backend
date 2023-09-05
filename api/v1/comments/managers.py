from django.db import models


class BaseCommentManager(models.Manager):
    def newest(self):
        return self.order_by("-created_at")
