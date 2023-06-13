import pytest
from django.utils.text import slugify
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_store_creation():
    name = 'Test Store'
    store = mixer.blend('stores.Store', name=name)

    assert store.views == 0
    assert store.slug == slugify(name)


@pytest.mark.django_db
def test_store_get_comments(store):
    objects_num = 5
    mixer.cycle(objects_num).blend('interactions.StoreComment', store=store)
    comments = store.get_comments()
    assert len(comments) == objects_num


@pytest.mark.django_db
def test_store_popular_products(store):
    objects_num = 5
    mixer.cycle(objects_num).blend('products.Product', store=store, views=mixer.RANDOM)
    popular_products = store.popular_products()
    assert len(popular_products) == objects_num


if __name__ == '__main__':
    pytest.main()
