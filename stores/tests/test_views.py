import os

import pytest
from django.conf import settings

from interactions.models import StoreComment
from stores.models import Store
from users.models import User


@pytest.fixture
def store():
    store = Store.objects.create(
        name='Test Store',
        slug='test_store',
        logo=os.path.join(settings.STATIC_URL, 'images/store_test_logo.png'),
    )
    return store


@pytest.fixture
def user():
    user = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')
    return user


@pytest.fixture
def store_comment(store, user):
    comment = StoreComment.objects.create(store=store, user=user, comment='Test Comment')
    return comment


@pytest.mark.django_db
def test_store_detail_view(client, store):
    url = store.get_absolute_url()

    response = client.get(url)

    assert response.status_code == 200

    assert store.name in response.content.decode()

# @pytest.mark.django_db
# def test_store_detail_view_with_comment(client, store, store_comment):
#     # Создаем URL для просмотра деталей магазина
#     url = reverse('store-detail', kwargs={'pk': store.pk})
#
#     # Отправляем GET-запрос к URL
#     response = client.get(url)
#
#     # Проверяем, что запрос завершился успешно
#     assert response.status_code == 200
#
#     # Проверяем, что на странице отображается комментарий
#     assert store_comment.comment in response.content.decode()
