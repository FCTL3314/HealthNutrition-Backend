from stores.models import Store
from users.signals import BaseUpdateSlugSignal


class StoreUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Store
    slug_related_field = "name"


store_update_slug_signal = StoreUpdateSlugSignal()
