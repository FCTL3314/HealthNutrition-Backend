from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Min

User = get_user_model()


def get_comparison_group_model() -> type:
    return apps.get_model(app_label="comparisons", model_name="ComparisonGroup")


def get_comparison_model() -> type:
    return apps.get_model(app_label="comparisons", model_name="Comparison")


def calculate_new_comparison_group_position(author: User) -> int:
    """
    Gets the minimum value of the position field of
    the ComparisonGroup model, then decreases the
    resulting value by 1 so that the newly created
    object is the first in position.
    """
    min_position = (
        get_comparison_group_model()  # noqa
        .objects.filter(author=author)
        .aggregate(Min("position"))["position__min"]
        or 0
    )
    return min_position - 1
