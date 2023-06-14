from products.models import Product, ProductType
from users.signals import BaseUpdateSlugSignal


class ProductUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Product
    slug_related_field = 'name'


class ProductTypeUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = ProductType
    slug_related_field = 'name'


product_update_slug_signal = ProductUpdateSlugSignal()
product_type_update_slug_signal = ProductTypeUpdateSlugSignal()
