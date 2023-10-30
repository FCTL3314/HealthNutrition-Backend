from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.urls import reverse
from mixer.backend.django import mixer

from api.utils.tests import get_auth_header
from api.v1.comments.constants import COMMENTS_PAGINATE_BY
from api.v1.comments.models import BaseCommentModel, ProductComment, StoreComment
from api.v1.products.models import Product
from api.v1.stores.models import Store

User = get_user_model()


PRODUCT_COMMENTS = "api:v1:comments:product-list"
STORE_COMMENTS = "api:v1:comments:store-list"


@pytest.mark.django_db
@pytest.mark.parametrize(
    (
        "path,"
        "comment_model,"
        "comment_related_model,"
        "get_related_kwargs,"
        "param_arg"
    ),
    [
        (
            reverse(PRODUCT_COMMENTS),
            ProductComment,
            Product,
            lambda product: {"product_id": product.id},
            "product_id",
        ),
        (
            reverse(STORE_COMMENTS),
            StoreComment,
            Store,
            lambda store: {"store_id": store.id},
            "store_id",
        ),
    ],
)
def test_comment_list(
    client,
    path: str,
    comment_model: type[BaseCommentModel],
    comment_related_model: type[Model],
    get_related_kwargs: callable,
    param_arg: str,
):
    comment_related_object = mixer.blend(comment_related_model)
    mixer.cycle(COMMENTS_PAGINATE_BY * 2).blend(
        comment_model,
        level=0,
        **get_related_kwargs(comment_related_object),
    )

    response = client.get(
        path,
        data={param_arg: comment_related_object.id},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.data["results"]) == COMMENTS_PAGINATE_BY


@pytest.mark.django_db
@pytest.mark.parametrize(
    (
        "path,"
        "comment_model,"
        "comment_related_model,"
        "get_related_kwargs,"
        "param_arg"
    ),
    [
        (
            reverse(PRODUCT_COMMENTS),
            ProductComment,
            Product,
            lambda product: {"product_id": product.id},
            "product_id",
        ),
        (
            reverse(STORE_COMMENTS),
            StoreComment,
            Store,
            lambda store: {"store_id": store.id},
            "store_id",
        ),
    ],
)
def test_comment_children_list(
    client,
    path: str,
    comment_model: type[BaseCommentModel],
    comment_related_model: type[Model],
    get_related_kwargs: callable,
    param_arg: str,
):
    """
    Tests the return of a list of children of a
    particular comment.
    """
    comment_related_object = mixer.blend(comment_related_model)

    parent_comment = comment_model.objects.create(
        **get_related_kwargs(comment_related_object)
    )

    children_count = 6
    children_to_create = [
        comment_model(
            parent_id=parent_comment.id,
            level=0,
            lft=0,
            rght=0,
            tree_id=0,
            **get_related_kwargs(comment_related_object),
        )
        for _ in range(children_count)
    ]

    comment_model.objects.bulk_create(children_to_create)

    response = client.get(
        path,
        data={
            param_arg: comment_related_object.id,
            "parent_id": parent_comment.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data["count"] == children_count


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path, comment_model, comment_related_model, model_id_key",
    [
        (reverse(PRODUCT_COMMENTS), ProductComment, Product, "product_id"),
        (reverse(STORE_COMMENTS), StoreComment, Store, "store_id"),
    ],
)
def test_comment_create(
    client,
    path: str,
    comment_model: type[BaseCommentModel],
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
    "comment_model",
    [
        ProductComment,
        StoreComment,
    ],
)
def test_comment_update(
    client,
    comment_model: type[BaseCommentModel],
    comment_text: str,
    admin_user: User,
):
    comment_object = mixer.blend(comment_model)

    response = client.patch(
        comment_object.get_absolute_url(),
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
    "comment_model",
    [
        ProductComment,
        StoreComment,
    ],
)
def test_comment_delete(
    client,
    comment_model: type[BaseCommentModel],
    admin_user: User,
):
    comment_object = mixer.blend(comment_model)

    path = comment_object.get_absolute_url()

    response = client.delete(path, **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert comment_model.objects.count() == 0


if __name__ == "__main__":
    pytest.main()
