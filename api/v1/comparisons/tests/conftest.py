import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.v1.comparisons.models import ComparisonGroup, Comparison

User = get_user_model()

COMPARISONS_AMOUNT = 5


def create_comparisons_for_comparison_group(
    comparison_group_id: int,
) -> list[Comparison]:
    return mixer.cycle(COMPARISONS_AMOUNT).blend(
        "comparisons.Comparison", comparison_group__id=comparison_group_id
    )


@pytest.fixture
def comparison_group() -> ComparisonGroup:
    return mixer.blend("comparisons.ComparisonGroup")
