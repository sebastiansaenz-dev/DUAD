# Exercise 5

my_numbers = []

total_nums = int(input("Enter how many numbers the list will have: "))

for index in range(total_nums):
    num = int(input("Enter a number: "))
    my_numbers.append(num)

max_number = my_numbers[0]

for number in my_numbers:
    if number > max_number:
        max_number = number

print(my_numbers)
print(f'the greatest number is {max_number}')
