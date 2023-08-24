import pytest
from mixer.backend.django import mixer

from api.v1.comments.constants import COMMENTS_PAGINATE_BY


@pytest.fixture()
def product_comment():
    return mixer.blend("comments.ProductComment")


@pytest.fixture()
def product_comments():
    return mixer.cycle(COMMENTS_PAGINATE_BY * 2).blend("comments.ProductComment")


@pytest.fixture()
def store_comment():
    return mixer.blend("comments.StoreComment")


@pytest.fixture()
def store_comments():
    return mixer.cycle(COMMENTS_PAGINATE_BY * 2).blend("comments.StoreComment")


@pytest.fixture()
def comment_text():
    return "Test comment text"
