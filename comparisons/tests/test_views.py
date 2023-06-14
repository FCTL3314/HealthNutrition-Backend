import pytest
from django.conf import settings
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_comparison_product_type_list_view(client, user, product_types):
    client.force_login(user)

    for product_type in product_types:
        product = mixer.blend('products.Product', product_type=product_type)
        mixer.blend('comparisons.Comparison', user=user, product=product)

    path = reverse('comparisons:product-type-comparisons')

    response = client.get(path)

    context_object_list = response.context_data.get('object_list')

    assert response.status_code == 200
    assert len(context_object_list) == len(product_types[:settings.PRODUCT_TYPES_PAGINATE_BY])


@pytest.mark.django_db
def test_comparison_product_list_view(client, user, product_type):
    client.force_login(user)

    products = mixer.cycle(5).blend('products.Product', product_type=product_type)

    for product in products:
        mixer.blend('comparisons.Comparison', user=user, product=product)

    path = reverse('comparisons:product-comparisons', args=(product_type.slug,))

    response = client.get(path)

    context_object_list = response.context_data.get('object_list')

    assert response.status_code == 200
    assert len(context_object_list) == len(products)


if __name__ == '__main__':
    pytest.main()
