
# Exercise 5 

def count_upper_lower(string):
    counter_lowercase = 0
    counter_uppercase = 0

    for char in string:
        if char.islower():
            counter_lowercase += 1
        elif char.isupper():
            counter_uppercase += 1

    print(f'there are {counter_uppercase} uppercase letters and {counter_lowercase} lowercase letters')

my_string = input('enter a string: ')

count_upper_lower(my_string)