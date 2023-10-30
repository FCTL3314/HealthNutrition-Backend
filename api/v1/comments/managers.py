from django.db.models import QuerySet
from mptt.querysets import TreeQuerySet


class BaseCommentQuerySet(TreeQuerySet):
    def newest(self) -> QuerySet:
        """
        Returns newest comments by the date.
        """
        return self.order_by("-created_at")
