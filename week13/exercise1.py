


def get_parameters_and_returns(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            print(arg)
        function_return = func(*args, **kwargs)
        print(f'return of the function: {function_return}')
        print(f'kwargs: {kwargs}')
    return wrapper

@get_parameters_and_returns
def parameters(*args, **kwargs):
    return 'args and kwargs printed'


parameters('hello world', 'hola mundo', parameter='hello', parameter2='helloworld')