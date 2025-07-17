

def check_parameters_are_numbers(func):
    def wrapper(*args):
        try:
            integer_arguments = []
            for arg in args:
                int_arg = int(arg)
                integer_arguments.append(int_arg)
            func(*integer_arguments)
        except ValueError as error:
            print(error)
            print('one of the arguments is not a number')
    return wrapper



@check_parameters_are_numbers
def nums(*args):
    for arg in args:
        print(arg)


nums(2, 3, 5, '4')