
# Exercise 3

keys_list = ['class', 'phone']

student = {
    'name': 'Sebastian',
    'age': 18,
    'class': 'B1',
    'email': 'sebas@gmail.com',
    'phone': '123456789'
}

for key in keys_list:
    student.pop(key)

print(student)