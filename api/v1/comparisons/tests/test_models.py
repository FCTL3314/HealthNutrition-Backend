import pytest

from comparisons.models import Comparison


@pytest.mark.django_db
def test_comparison_manager_product_types(user, comparisons):
    expected = {comparison.product.product_type.id for comparison in comparisons}
    actual = Comparison.objects.product_types()

    assert len(expected) == len(actual)


if __name__ == "__main__":
    pytest.main()
