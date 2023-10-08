from api.base.services import BaseViewsIncreaseService
from api.v1.products.constants import (
    PRODUCT_VIEW_CACHE_TIME,
    PRODUCT_TYPE_VIEW_CACHE_TIME,
)


class ProductViewsIncreaseService(BaseViewsIncreaseService):
    view_cache_time = PRODUCT_VIEW_CACHE_TIME

    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_id:{self._instance.id}"


class ProductTypeViewsIncreaseService(BaseViewsIncreaseService):
    view_cache_time = PRODUCT_TYPE_VIEW_CACHE_TIME

    def get_cache_key(self) -> str:
        return f"ip:{self._user_ip_address}-product_type_id:{self._instance.id}"
