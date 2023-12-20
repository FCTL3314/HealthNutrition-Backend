from collections import namedtuple

Error = namedtuple("Error", ("message", "code"))

ATTRIBUTE_MUST_BE_OVERRIDDEN = (
    "The '{attribute_name:}' attribute of the {class_name:} class must be overridden."
)


ATTRIBUTE_OR_METHOD_MUST_BE_OVERRIDDEN = (
    "'{class_name:}' should either override a `{attribute_name:}` attribute, or override "
    "the `{method_name:}` method."
)
