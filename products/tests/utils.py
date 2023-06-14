from mixer.backend.django import mixer


def create_products_for_product_types(product_types):
    for product_type in product_types:
        mixer.blend('products.Product', product_type=product_type)
