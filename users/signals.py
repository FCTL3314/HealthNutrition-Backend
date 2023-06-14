from common.signals import BaseUpdateSlugSignal
from users.models import User


class UserUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = User
    slug_related_field = "username"


user_update_slug_signal = UserUpdateSlugSignal()
