from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.urls import reverse
from mixer.backend.django import mixer

from api.utils.tests import get_auth_header
from api.v1.comments.constants import COMMENTS_PAGINATE_BY
from api.v1.comments.models import Comment
from api.v1.products.models import Product
from api.v1.stores.models import Store

User = get_user_model()


COMMENTS_PATTERN = "api:v1:comments:comments-list"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "content_type_model,",
    [Product, Store],
)
def test_comment_list(client, content_type_model: type[Model]):
    content_object = mixer.blend(content_type_model)

    mixer.cycle(COMMENTS_PAGINATE_BY * 2).blend(
        Comment,
        content_object=content_object,
        level=0,
    )

    response = client.get(
        reverse(COMMENTS_PATTERN),
        data={
            "object_id": content_object.id,
            "content_type": content_type_model._meta.model_name,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.data["results"]) == COMMENTS_PAGINATE_BY


@pytest.mark.django_db
@pytest.mark.parametrize(
    "content_type_model,",
    [Product, Store],
)
def test_comment_children_list(
    client,
    content_type_model: type[Model],
):
    """
    Tests the return of a list of children of a
    particular comment.
    """
    content_object = mixer.blend(content_type_model)

    parent_comment = mixer.blend(Comment, content_object=content_object)

    children_count = 6
    children_to_create = [
        Comment(
            parent_id=parent_comment.id,
            level=0,
            lft=0,
            rght=0,
            tree_id=0,
            content_object=content_object,
        )
        for _ in range(children_count)
    ]

    Comment.objects.bulk_create(children_to_create)

    response = client.get(
        reverse(COMMENTS_PATTERN),
        data={
            "object_id": content_object.id,
            "content_type": content_type_model._meta.model_name,
            "parent_id": parent_comment.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data["count"] == children_count


@pytest.mark.django_db
@pytest.mark.parametrize(
    "content_type_model",
    [Product, Store],
)
def test_comment_create(
    client,
    admin_user: User,
    content_type_model: type[Model],
    comment_text: str,
):
    content_object = mixer.blend(content_type_model)

    response = client.post(
        reverse(COMMENTS_PATTERN),
        data={
            "text": comment_text,
            "object_id": content_object.id,
            "content_type": content_type_model._meta.model_name,
        },
        content_type="application/json",
        **get_auth_header(admin_user),
    )

    assert response.status_code == HTTPStatus.CREATED
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_comment_update(
    client,
    comment: Comment,
    comment_text: str,
    admin_user: User,
):
    response = client.patch(
        comment.get_absolute_url(),
        data={"text": comment_text},
        content_type="application/json",
        **get_auth_header(admin_user),
    )

    assert response.status_code == HTTPStatus.OK
    comment.refresh_from_db()
    assert comment.text == comment_text
    assert comment.edited is True


@pytest.mark.django_db
def test_comment_delete(
    client,
    comment: Comment,
    admin_user: User,
):
    response = client.delete(comment.get_absolute_url(), **get_auth_header(admin_user))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert Comment.objects.count() == 0


if __name__ == "__main__":
    pytest.main()
