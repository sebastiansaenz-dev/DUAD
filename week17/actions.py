


def is_valid_string(value):
    try:
        int(value) or value.strip() == None
        return False
    except ValueError:
        return True

def is_valid_int(value):
    try:
        if int(value) and int(value) > 0:
            return True
    except ValueError:
        return False
    
