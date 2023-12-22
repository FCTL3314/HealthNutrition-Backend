import pytest
from django.contrib.auth import get_user_model

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.services.models import calculate_new_comparison_group_position
from api.v1.comparisons.tests.conftest import create_comparisons_for_comparison_group

User = get_user_model()


@pytest.mark.django_db
def test_comparison_manager_products(comparison_group: ComparisonGroup):
    comparisons = create_comparisons_for_comparison_group(comparison_group.id)

    expected = {comparison.product for comparison in comparisons}
    actual = Comparison.objects.products(comparison_group.id)  # noqa

    assert len(expected) == len(actual)


@pytest.mark.django_db
def test_calculate_new_comparison_group_position(comparison_group: ComparisonGroup):
    current_group_position = comparison_group.position
    new_group_position = calculate_new_comparison_group_position(
        comparison_group.author
    )
    assert new_group_position == (current_group_position - 1)


if __name__ == "__main__":
    pytest.main()
