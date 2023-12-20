from django.db import models

from api.utils.text import slugify_unique
from api.v1.comparisons.managers import ComparisonManager, ComparisonGroupManager
from api.v1.comparisons.services.models import calculate_new_comparison_group_position


class ComparisonGroup(models.Model):
    """
    Unites compared products into a specific
    comparison group.
    """

    name = models.CharField(max_length=32)
    author = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    position = models.IntegerField(null=True)

    objects = ComparisonGroupManager()

    class Meta:
        indexes = (
            models.Index(
                fields=("position",),
            ),
            models.Index(
                fields=("created_at",),
            ),
        )

    def __str__(self):
        return f"Name: {self.name} | Author: {self.author.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unique(self.name, ComparisonGroup)
        if self.position is None:
            self.position = calculate_new_comparison_group_position(self.author)
        return super().save(*args, **kwargs)


class Comparison(models.Model):
    """
    Represents a comparison of a specific product
    for a specific comparison group.
    """

    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    creator = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    comparison_group = models.ForeignKey(
        to="comparisons.ComparisonGroup",
        related_name="comparisons",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ComparisonManager()

    class Meta:
        unique_together = ("product", "comparison_group", "creator")

    def __str__(self):
        return f"Group: {self.comparison_group.name} | Product: {self.product.name}"
