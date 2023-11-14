from dataclasses import dataclass

PRICE_ROUNDING = 2
PRODUCTS_PAGINATE_BY = 16
PRODUCTS_ORDERING = ("name",)
PRODUCT_VIEW_CACHE_TIME = 60 * 60


@dataclass(frozen=True)
class NutritionHealthfulnessImportance:
    PROTEIN = 3
    FAT = 2
    CARBS = 1
