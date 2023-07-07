import pytest

from rest_framework.test import APIRequestFactory


@pytest.fixture()
def api_client():
    return APIRequestFactory()
