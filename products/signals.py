from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from products.models import Product


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_product_type_aggregates(instance, **kwargs):
    product_type = instance.product_type
    product_type.update_aggregates()
