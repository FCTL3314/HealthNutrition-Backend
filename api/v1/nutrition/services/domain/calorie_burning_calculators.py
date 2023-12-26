from typing import Protocol

from api.v1.user_profiles.constants import DEFAULT_USER_BODY_WEIGHT_KG


class ExerciseCalorieBurningCalculatorProto(Protocol):
    """
    An interface for services for calculating the
    time it will take to burn a provided calories
    from a specific exercise.
    """

    def calculate(self, calories: int | float) -> int | float:
        ...

    def _get_calories_per_hour_of_exercise(self) -> int | float:
        ...


class ExerciseCalorieBurningCalculator(ExerciseCalorieBurningCalculatorProto):
    """
    Basic class for calculating calorie burn hours
    for a specific metabolic equivalent and body
    weight.
    """

    DEFAULT_BODY_WEIGHT_KG = DEFAULT_USER_BODY_WEIGHT_KG

    def __init__(
        self,
        metabolic_equivalent: int | float,
        body_weight: int | float | None = None,
    ):
        self._met = metabolic_equivalent
        self._body_weight = (
            self.DEFAULT_BODY_WEIGHT_KG if body_weight is None else body_weight
        )

    def calculate(self, calories: int | float) -> int | float:
        """
        Returns hours it will take to burn calories.
        """
        calories_per_hour_of_exercise = self._get_calories_per_hour_of_exercise()
        return calories / calories_per_hour_of_exercise

    def _get_calories_per_hour_of_exercise(self) -> int | float:
        """
        Returns the calories you need to spend on
        doing the exercise for 1 hour.
        """
        return self._met * self._body_weight


class WalkingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    """
    Calculates the hours it takes to burn calories
    while walking.
    """

    def __init__(self, body_weight: int | float | None = None):
        super().__init__(
            body_weight=body_weight,
            metabolic_equivalent=4,
        )


class RunningCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    """
    Calculates the hours it takes to burn calories
    while running.
    """

    def __init__(self, body_weight: int | float | None = None):
        super().__init__(
            body_weight=body_weight,
            metabolic_equivalent=7.5,
        )


class CyclingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    """
    Calculates the hours it takes to burn calories
    while cycling.
    """

    def __init__(self, body_weight: int | float | None = None):
        super().__init__(
            body_weight=body_weight,
            metabolic_equivalent=5.5,
        )
