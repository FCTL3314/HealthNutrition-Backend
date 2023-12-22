from typing import Protocol


class ExerciseCalorieBurningCalculatorProto(Protocol):
    """
    An interface for services for calculating the time
    it will take to burn a provided calories from a
    specific exercise.
    """

    def calculate(self, calories: int | float) -> int | float:
        ...

    def _get_calories_spent_on_exercise(self) -> int | float:
        ...


class ExerciseCalorieBurningCalculator(ExerciseCalorieBurningCalculatorProto):
    DEFAULT_PERSON_WEIGHT_KG = 70

    def __init__(
        self,
        metabolic_equivalent: int | float,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        self._met = metabolic_equivalent
        self._exercise_hours = exercise_hours
        self._body_weight = (
            self.DEFAULT_PERSON_WEIGHT_KG if body_weight is None else body_weight
        )

    def calculate(self, calories: int | float) -> int | float:
        calories_spent_on_exercise = self._get_calories_spent_on_exercise()
        return calories / calories_spent_on_exercise

    def _get_calories_spent_on_exercise(self) -> int | float:
        return (self._met * self._body_weight) * self._exercise_hours


class WalkingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=4,
        )


class RunningCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=7.5,
        )


class CyclingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=5.5,
        )
