
#Exercise 3

def sum_list(numbers):
    total = 0
    for number in range(0, len(numbers)):
        total += numbers[number]
    print(total)

def get_list_numbers():
    num_list = []
    total_nums = int(input('enter how many numbers will the list have: '))
    for num in range(total_nums):
        num_list.append(int(input(f'enter number: ')))
    return num_list

sum_list(get_list_numbers())