from api.v1.stores.models import Store
from api.v1.users.signals import BaseUpdateSlugSignal


class StoreUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Store
    slug_related_field = "name"


store_update_slug_signal = StoreUpdateSlugSignal()
