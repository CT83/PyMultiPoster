def is_string_empty(s):
    return str(s) in 'None' or str(s) in "" or s is None


def is_string_populated(s):
    return not is_string_empty(s)
