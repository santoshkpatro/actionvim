def cast_to_boolean(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value_lower = value.lower()
        if value_lower in ("true", "t", "yes", "y", "1"):
            return True
        elif value_lower in ("false", "f", "no", "n", "0"):
            return False
    return bool(value)
