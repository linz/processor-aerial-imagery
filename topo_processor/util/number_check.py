def check_for_number(value):
    try:
        int_number = int(value)
        return int_number
    except ValueError:
        try:
            float_number = float(value)
            return float_number
        except ValueError:
            return value
