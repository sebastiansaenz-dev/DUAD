# Exercise 2

name = input('enter the first name: ')
last_name = input('enter the last name: ')
age = int(input('enter the age: '))

if (age <= 1):
    if (age < 0):
        print(f"{name} {last_name} hasn't been born yet")
    else:
        print(f'{name} {last_name} is an infant')
elif (age <= 4):
    print(f'{name} {last_name} is a toddler')
elif (age <= 12):
    print(f'{name} {last_name} is a child')
elif (age < 18):
    print(f'{name} {last_name} is a teenager')
elif (age <= 25):
    print(f'{name} {last_name} is a young adult')
elif (age < 60):
    print(f'{name} {last_name} is a middle adult')
else:
    print(f'{name} {last_name} is a senior adult')