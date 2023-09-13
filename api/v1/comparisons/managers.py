from django.contrib.auth import get_user_model
from django.db import models

from api.v1.products.models import Product, ProductType

User = get_user_model()


class ComparisonQuerySet(models.QuerySet):
    def product_types(self, user: User):
        product_type_ids = self.filter(user=user).values_list(
            "product__product_type", flat=True
        )
        return ProductType.objects.filter(id__in=product_type_ids)

    def products(self, product_type: ProductType, user: User):
        product_ids = self.filter(
            product__product_type=product_type, user=user
        ).values_list("product", flat=True)
        return Product.objects.filter(id__in=product_ids)


class ComparisonManager(models.Manager):
    _queryset_class = ComparisonQuerySet

    def product_types(self, user: User):
        return self.all().product_types(user)

    def products(self, product_type: ProductType, user: User):
        return self.all().products(product_type, user)
