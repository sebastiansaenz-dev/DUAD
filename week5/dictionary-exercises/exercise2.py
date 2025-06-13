
# Exercise 2

user_info = {}

first_list = ['name', 'age', 'role']
second_list = ['Sebastian Saenz', 18, 'student']

for element in range(0, len(first_list)):
    user_info[first_list[element]] = second_list[element]

print(user_info)