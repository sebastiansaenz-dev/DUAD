# Exercise 4

def reverse_string(user_string):
    final_string = ''
    for char in range(len(user_string) -1, -1, -1):
        final_string += user_string[char]
    print(final_string)

my_string = (input('enter your string: '))


reverse_string(my_string)