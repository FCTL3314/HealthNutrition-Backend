from api.base.services import (
    BaseViewsIncreaseService,
)
from api.v1.categories.constants import CATEGORY_VIEW_CACHE_TIME


class CategoryViewsIncreaseService(BaseViewsIncreaseService):
    view_cache_time = CATEGORY_VIEW_CACHE_TIME

    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_type_id:{self._instance.id}"
