from products.models import Product, ProductType
from users.signals import BaseUpdateSlugSignal


class ProductUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Product
    field_to_slugify = 'name'


class ProductTypeUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = ProductType
    field_to_slugify = 'name'


product_update_slug_signal = ProductUpdateSlugSignal()
product_type_update_slug_signal = ProductTypeUpdateSlugSignal()
