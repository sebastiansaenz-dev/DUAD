


def is_valid_string(value):
    value = str(value)

    if value.strip() == '':
        return False


    try:
        int(value)
        return False
    except ValueError:
        return True

def is_valid_int(value):
    try:
        if int(value) and int(value) > 0:
            return True
    except ValueError:
        return False
    
