import math

# Exercise 7

def get_list_numbers():
    num_list = []
    total_nums = int(input('enter how many numbers will the list have: '))
    for num in range(total_nums):
        num_list.append(int(input(f'enter number: ')))
    return num_list


def verify_prime_numbers(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    else:
        counter = 2
            
        while counter <= int(math.sqrt(num)):
            if num % counter != 0:
                counter += 1
            elif num % counter == 0:
                return False
        return True


def get_prime_numbers(list):
    new_list = []
    for num in list:
        if verify_prime_numbers(num):
            new_list.append(num)
    return new_list

#print(f'{get_prime_numbers(get_list_numbers())}')
