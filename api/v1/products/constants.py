from dataclasses import dataclass

PRICE_ROUNDING = 2
PRODUCTS_PAGINATE_BY = 3
PRODUCTS_ORDERING = ("name",)
PRODUCT_VIEW_CACHE_TIME = 60 * 60


@dataclass(frozen=True)
class NutritionHealthfulnessCoefficient:
    CALORIES = 1.0
    PROTEIN = 2.8
    FAT = 1.8
    CARBS = 1.2
