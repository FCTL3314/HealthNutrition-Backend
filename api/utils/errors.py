from collections import namedtuple

ErrorMessage = namedtuple("ErrorMessage", ("message", "code"))

ATTRIBUTE_UNDEFINED_TEMPLATE = (
    "The '{class_name:}' class does not have a '{attribute_name:}' attribute defined."
)
