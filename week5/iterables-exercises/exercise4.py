# Exercise 4

my_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11]

for index in range(len(my_numbers) -1, -1, -1):
    if my_numbers[index] % 2 != 0:
        my_numbers.pop(index)

print(my_numbers) 