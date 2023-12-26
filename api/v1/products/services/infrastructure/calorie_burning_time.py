from api.v1.nutrition.serializers import CaloriesBurningTimeSerializer
from api.v1.nutrition.services.infrastructure.humanized_calorie_burning_calculators import (
    CalorieBurningCalculatorForBasicExercises,
)


def get_calories_burning_time_for_basic_exercises(
    calories: int,
    body_weight: int | float | None = None,
) -> dict[str, str]:
    """
    Validates and returns a dictionary with the burn
    times of the provided calories for basic exercises.
    """
    calories_burning_calculator = CalorieBurningCalculatorForBasicExercises(
        body_weight=body_weight
    )

    serializer = CaloriesBurningTimeSerializer(
        data=calories_burning_calculator.calculate_all(calories)
    )

    if not serializer.is_valid():
        raise ValueError(
            f"{CaloriesBurningTimeSerializer.__name__} received invalid data"
        )

    return serializer.validated_data
