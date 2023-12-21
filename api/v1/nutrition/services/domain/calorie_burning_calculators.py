from api.base.services import IService


class ExerciseCalorieBurningCalculator(IService):
    DEFAULT_PERSON_WEIGHT_KG = 70

    def __init__(
        self,
        calories: int | float,
        metabolic_equivalent: int | float,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        self.calories = calories
        self.met = metabolic_equivalent
        self.exercise_hours = exercise_hours
        self.body_weight = (
            self.DEFAULT_PERSON_WEIGHT_KG if body_weight is None else body_weight
        )

    def execute(self) -> int | float:
        calories_per_hour_of_exercise = self._get_calories_per_hour_of_exercise()
        return self.calories / calories_per_hour_of_exercise

    def _get_calories_per_hour_of_exercise(self) -> int | float:
        return (self.met * self.body_weight) * self.exercise_hours


class WalkingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        calories: int | float,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            calories,
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=4,
        )


class RunningCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        calories: int | float,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            calories,
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=7.5,
        )


class CyclingCalorieBurningCalculator(ExerciseCalorieBurningCalculator):
    def __init__(
        self,
        calories: int | float,
        exercise_hours: int | float = 1,
        body_weight: int | float | None = None,
    ):
        super().__init__(
            calories,
            exercise_hours=exercise_hours,
            body_weight=body_weight,
            metabolic_equivalent=5.5,
        )
