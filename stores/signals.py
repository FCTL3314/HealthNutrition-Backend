from stores.models import Store
from users.signals import BaseUpdateSlugSignal


class StoreUpdateSlugSignal(BaseUpdateSlugSignal):
    sender = Store
    slugify_field = 'name'
