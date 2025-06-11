
# Exercise 2


def first_function():
    variable = 10

#print(variable)
# Error because variable is not defined in the global scope


global_variable = 10

print(global_variable)

def second_function():
    global_variable = 20
    print(global_variable)

second_function()
# the global variable has been changed but it's not a good practice to modify global variables inside functions