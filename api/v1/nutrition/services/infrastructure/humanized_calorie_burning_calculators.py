from datetime import timedelta

from django.utils.timesince import timesince
from django.utils.timezone import now

from api.base.services import IService
from api.v1.nutrition.services.domain.calorie_burning_calculators import (
    WalkingCalorieBurningCalculator as RawWalkingCalorieBurningCalculator,
    RunningCalorieBurningCalculator as RawRunningCalorieBurningCalculator,
    CyclingCalorieBurningCalculator as RawCyclingCalorieBurningCalculator,
)


class HumanizedCalorieBurningCalculatorMixin(IService):
    def execute(self) -> str:
        burning_hours = super().execute()
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
