import pytest
from django.contrib.auth import get_user_model

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.tests.conftest import create_comparisons_for_comparison_group

User = get_user_model()


@pytest.mark.django_db
def test_comparison_manager_products(comparison_group: ComparisonGroup):
    comparisons = create_comparisons_for_comparison_group(comparison_group.id)

    expected = {comparison.product for comparison in comparisons}
    actual = Comparison.objects.products(comparison_group.id)

    assert len(expected) == len(actual)


if __name__ == "__main__":
    pytest.main()
