import pytest
from django.contrib.auth import get_user_model

from api.v1.comparisons.models import Comparison
from api.v1.comparisons.tests.conftest import create_user_comparisons

User = get_user_model()


@pytest.mark.django_db
def test_comparison_manager_product_types(user: User):
    comparisons = create_user_comparisons(user)

    expected = {comparison.product.product_type for comparison in comparisons}
    actual = Comparison.objects.product_types(user)

    assert len(expected) == len(actual)


if __name__ == "__main__":
    pytest.main()
