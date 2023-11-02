import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def comment():
    return mixer.blend("comments.Comment")


@pytest.fixture()
def comment_text():
    return "Test comment text"
