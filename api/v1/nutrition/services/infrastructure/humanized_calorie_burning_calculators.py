from datetime import timedelta
from typing import Protocol

from django.utils.timesince import timesince
from django.utils.timezone import now

from api.v1.nutrition.services.domain.calorie_burning_calculators import (
    WalkingCalorieBurningCalculator as RawWalkingCalorieBurningCalculator,
    RunningCalorieBurningCalculator as RawRunningCalorieBurningCalculator,
    CyclingCalorieBurningCalculator as RawCyclingCalorieBurningCalculator,
    ExerciseCalorieBurningCalculatorProto,
)


class HumanizedCalorieBurningCalculatorProto(ExerciseCalorieBurningCalculatorProto):
    """
    An extension to the 'ExerciseCalorieBurningCalculatorProto'
    interface that adds the 'calculate_humanized' method,
    which allows to get humanized calorie burning time.
    """

    def calculate_humanized(self, calories: int | float) -> str:
        ...


class HumanizedCalorieBurningCalculatorMixin(HumanizedCalorieBurningCalculatorProto):
    """
    A mixin that converts a float calorie burning
    hours into a timesince string.
    """

    def calculate_humanized(self, calories: int | float) -> str:
        burning_hours = self.calculate(calories)
        return timesince(now() - timedelta(hours=burning_hours))


class WalkingCalorieBurningCalculator(
    HumanizedCalorieBurningCalculatorMixin, RawWalkingCalorieBurningCalculator
):
    ...


class RunningCalorieBurningCalculator(
    HumanizedCalorieBurningCalculatorMixin, RawRunningCalorieBurningCalculator
):
    ...


class CyclingCalorieBurningCalculator(
    HumanizedCalorieBurningCalculatorMixin, RawCyclingCalorieBurningCalculator
):
    ...


class CalorieBurningCalculatorForBasicExercisesProto(Protocol):
    def calculate_walking(self, calories: int | float) -> str:
        ...

    def calculate_running(self, calories: int | float) -> str:
        ...

    def calculate_cycling(self, calories: int | float) -> str:
        ...


class CalorieBurningCalculatorForBasicExercises(
    CalorieBurningCalculatorForBasicExercisesProto
):
    """
    Implementation of a façade pattern for combining
    basic exercises for burning calories: Walking,
    running, cycling. Implements calculate_walking,
    calculate_running, calculate_cycling methods that
    return humanized time value.
    """

    def __init__(
        self, exercise_hours: int | float = 1, body_weight: int | float | None = None
    ):
        self._walking_calculator = WalkingCalorieBurningCalculator(
            exercise_hours=exercise_hours, body_weight=body_weight
        )
        self._running_calculator = RunningCalorieBurningCalculator(
            exercise_hours=exercise_hours, body_weight=body_weight
        )
        self._cycling_calculator = CyclingCalorieBurningCalculator(
            exercise_hours=exercise_hours, body_weight=body_weight
        )

    def calculate_walking(self, calories: int | float) -> str:
        return self._walking_calculator.calculate_humanized(calories)

    def calculate_running(self, calories: int | float) -> str:
        return self._running_calculator.calculate_humanized(calories)

    def calculate_cycling(self, calories: int | float) -> str:
        return self._cycling_calculator.calculate_humanized(calories)
