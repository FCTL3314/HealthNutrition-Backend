from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.urls import reverse
from mixer.backend.django import mixer

from api.utils.tests import get_auth_header
from api.v1.comments.constants import COMMENTS_PAGINATE_BY
from api.v1.comments.models import BaseComment, ProductComment, StoreComment
from api.v1.products.models import Product
from api.v1.stores.models import Store

User = get_user_model()


PRODUCT_COMMENT_DETAIL = "api:v1:comments:product-detail"
PRODUCT_COMMENTS = "api:v1:comments:product-list"

STORE_COMMENT_DETAIL = "api:v1:comments:store-detail"
STORE_COMMENTS = "api:v1:comments:store-list"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,comment_model",
    [
        (reverse(PRODUCT_COMMENTS), ProductComment),
        (reverse(STORE_COMMENTS), StoreComment),
    ],
)
def test_comment_list(client, path: str, comment_model: BaseComment):
    mixer.cycle(COMMENTS_PAGINATE_BY * 2).blend(comment_model)

    response = client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert len(response.data["results"]) == COMMENTS_PAGINATE_BY


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,comment_model,comment_related_model,model_id_key",
    [
        (reverse(PRODUCT_COMMENTS), ProductComment, Product, "product_id"),
        (reverse(STORE_COMMENTS), StoreComment, Store, "store_id"),
    ],
)
def test_comment_create(
    client,
    path: str,
    comment_model: type[BaseComment],
    comment_related_model: type[Model],
    model_id_key: str,
    comment_text: str,
    admin_user: User,
):
    comment_related_object = mixer.blend(comment_related_model)

    data = {
        "text": comment_text,
        model_id_key: comment_related_object.id,
    }

    response = client.post(
        path,
        data=data,
        content_type="application/json",
        **get_auth_header(admin_user),
    )

    assert response.status_code == HTTPStatus.CREATED
    assert comment_model.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_pattern,comment_model",
    [
        (PRODUCT_COMMENT_DETAIL, ProductComment),
        (STORE_COMMENT_DETAIL, StoreComment),
    ],
)
def test_comment_update(
    client,
    url_pattern: str,
    comment_model: type[BaseComment],
    comment_text: str,
    admin_user: User,
):
    comment_object = mixer.blend(comment_model)

    path = reverse(url_pattern, args=(comment_object.id,))

    response = client.patch(
        path,
        data={"text": comment_text},
        content_type="application/json",
        **get_auth_header(admin_user),
    )

    assert response.status_code == HTTPStatus.OK
    comment_object.refresh_from_db()
    assert comment_object.text == comment_text
    assert comment_object.edited is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_pattern,comment_model",
    [
        (PRODUCT_COMMENT_DETAIL, ProductComment),
        (STORE_COMMENT_DETAIL, StoreComment),
    ],
)
def test_comment_delete(
    client,
    url_pattern: str,
    comment_model: type[BaseComment],
    admin_user: User,
):
    comment_object = mixer.blend(comment_model)

    path = reverse(url_pattern, args=(comment_object.id,))

    response = client.delete(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert comment_model.objects.count() == 0


if __name__ == "__main__":
    pytest.main()
