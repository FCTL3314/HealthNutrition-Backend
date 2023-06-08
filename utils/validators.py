def validate_attribute_not_none(attribute, error_attribute_name):
    if attribute is None:
        raise AttributeError(f'Attribute {error_attribute_name} cannot be None.')
