from api.base.services import BaseViewsIncreaseService
from api.v1.stores.constants import STORE_VIEW_CACHE_TIME


class StoreViewsIncreaseService(BaseViewsIncreaseService):
    view_cache_time = STORE_VIEW_CACHE_TIME

    def get_cache_key(self) -> str:
        return f"address:{self._user_ip_address}-store_id:{self._instance.id}"
