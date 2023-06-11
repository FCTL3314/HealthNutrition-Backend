from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import reverse

from common.tests import common_detail_view_tests
from interactions.tests import ProductCommentTestFactory
from products.tests import ProductTestFactory, ProductTypeTestFactory


@pytest.fixture()
def product_type():
    return ProductTypeTestFactory()


@pytest.fixture()
def product_types():
    return ProductTypeTestFactory.create_batch(settings.PRODUCT_TYPES_PAGINATE_BY * 2)


@pytest.fixture()
def product():
    return ProductTestFactory()


@pytest.mark.django_db
def test_product_type_list_view(client, product_types):
    path = reverse('products:product-types')

    response = client.get(path)

    context_object_list = response.context_data.get('object_list')

    assert response.status_code == HTTPStatus.OK
    assert len(context_object_list) == len(product_types[:settings.PRODUCT_TYPES_PAGINATE_BY])


@pytest.mark.django_db
def test_product_list_view(client, product_type):
    products = ProductTestFactory.create_batch(settings.PRODUCTS_PAGINATE_BY * 2, product_type=product_type)

    path = reverse('products:products', args=(product_type.slug,))

    response = client.get(path)

    product_type.refresh_from_db()
    context_object_list = response.context_data.get('object_list')

    assert response.status_code == HTTPStatus.OK
    assert product_type.views == 1
    assert len(context_object_list) == len(products[:settings.PRODUCTS_PAGINATE_BY])


@pytest.mark.django_db
def test_product_detail_view(client, product):
    comments = ProductCommentTestFactory.create_batch(settings.COMMENTS_PAGINATE_BY * 2, product=product)

    path = product.get_absolute_url()

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    common_detail_view_tests(response, product, comments)


if __name__ == '__main__':
    pytest.main()
