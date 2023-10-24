from collections import namedtuple

Error = namedtuple("Error", ("message", "code"))

ATTRIBUTE_MUST_BE_OVERRIDDEN = (
    "The '{attribute_name:}' attribute of the {class_name:} class must be overridden."
)
