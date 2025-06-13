# Exercise 3

my_numbers = []

total_nums = int(input("Enter how many numbers the list will have: "))

for index in range(total_nums):
    num = int(input("Enter a number: "))
    my_numbers.append(num)

for index in range(len(my_numbers)):
    if index == 0:
        last_number = my_numbers[-1]
        first_number = my_numbers[0]

        my_numbers[-1] = first_number
        my_numbers[0] = last_number

print(my_numbers)