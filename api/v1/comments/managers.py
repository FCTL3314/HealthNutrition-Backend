from django.db.models import QuerySet
from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet


class CommentQuerySet(TreeQuerySet):
    def newest_first_order(self) -> QuerySet:
        """
        Returns newest comments by the date.
        """
        return self.order_by("-created_at")

    def top_level(self) -> QuerySet:
        """
        Returns all root comments of the comments
        tree.
        """
        return self.filter(level=0)


class CommentManager(TreeManager.from_queryset(CommentQuerySet)):
    ...
