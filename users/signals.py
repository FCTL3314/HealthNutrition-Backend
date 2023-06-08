from common.signals import BaseUpdateSlugSignal
from users.models import User


class UserUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = User
    field_to_slugify = 'username'


user_update_slug_signal = UserUpdateSlugSignal()
