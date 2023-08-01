import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def comparisons(user):
    return mixer.cycle(5).blend("comparisons.Comparison", user=user)
