from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

User = get_user_model()

COMPARISONS_AMOUNT = 5


def create_user_comparisons(user: User):
    return mixer.cycle(COMPARISONS_AMOUNT).blend("comparisons.Comparison", user=user)
