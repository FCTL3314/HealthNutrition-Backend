from datetime import datetime
from typing import Iterable


def is_datetime_attrs_equal(
    comparable_objects: Iterable[datetime],
    comparable_attrs: Iterable[str] = ("day", "hour", "minute", "second"),
) -> bool:
    """
    Allows to make an inaccurate comparison of datetime
    objects, the comparison is carried out only by the
    received attributes.

    Returns True if the 'comparable_attrs' attributes
    for each object in comparable_objects are the same,
    otherwise False.

    Use it when you want to compare the datetime object
    only by certain attributes, for example, only by day
    and hour.
    """
    for attr in comparable_attrs:
        values = set()
        for comparable_object in comparable_objects:
            value = getattr(comparable_object, attr)
            values.add(value)
            if len(values) > 1:
                return False
    return True


def round_datetime(
    datetime_to_round: datetime,
    attrs_to_round: Iterable[str] = ("microsecond",),
) -> datetime:
    """
    Rounds the provided attributes of the datetime
    object and returns the rounded object.
    """
    for attr_to_round in attrs_to_round:
        datetime_to_round = datetime_to_round.replace(**{attr_to_round: 0})
    return datetime_to_round
