from stores.models import Store
from users.signals import BaseUpdateSlugSignal


class StoreUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Store
    field_to_slugify = 'name'


store_update_slug_signal = StoreUpdateSlugSignal()
