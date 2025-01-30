def getattr_filter(object, attribute_name):
    if object is None:
        return None

    if attribute_name is None:
        return None

    nested_attributes = attribute_name.split(".")

    if len(nested_attributes) == 1:
        return getattr(object, attribute_name, None)

    value = object

    for attribute in nested_attributes:
        value = getattr(value, attribute, None)

    return value
