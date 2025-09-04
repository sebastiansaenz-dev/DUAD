


def is_valid_string(value):
    try:
        int(value)
        return False
    except ValueError:
        return True

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
    
