from django.db import models

from api.v1.comparisons.managers import ComparisonManager


class ComparisonGroup(models.Model):
    """
    Unites compared products into a specific
    comparison group.
    """

    name = models.CharField(max_length=32)
    author = models.ForeignKey(to="users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.author.username}"


class Comparison(models.Model):
    """
    Represents a comparison of a specific product
    for a specific comparison group.
    """

    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    creator = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    comparison_group = models.ForeignKey(
        to="comparisons.ComparisonGroup", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ComparisonManager()

    def __str__(self):
        return f"{self.comparison_group.name} | {self.product.name}"
