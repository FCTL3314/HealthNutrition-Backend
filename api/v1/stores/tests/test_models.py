import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
def test_store_popular_products(store):
    objects_num = 5
    mixer.cycle(objects_num).blend("products.Product", store=store, views=mixer.RANDOM)
    popular_products = store.popular_products()
    assert len(popular_products) == objects_num


if __name__ == "__main__":
    pytest.main()
