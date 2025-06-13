# Exercise 3

import random

secret_num = random.randint(1, 10)
user_num = int(input('enter a number: '))

while (secret_num != user_num):
    print('fail! try again')
    user_num = int(input('enter another number: '))
print('Congratulations! you guessed the number!')