
# Exercise week 7

#function who initialize the CLI calculator and has the menu
def initialize_calculator():
    actual_num = 0
    while True:
        print('1: Add')
        print('2: Subtract')
        print('3: Multiply')
        print('4: Divide')
        print('5: delete actual number')
        print('6: Exit')

        user_choice = input('Enter the number of your choice: ')
        while True:
            try:
                user_choice = int(user_choice)
                
                if 1 <= user_choice <= 6:
                    if user_choice == 1:
                        new_actual_num = sum_function(actual_num)
                        actual_num = new_actual_num
                        break
                    elif user_choice == 2:
                        new_actual_num = subtract_function(actual_num)
                        actual_num = new_actual_num
                        break
                    elif user_choice == 3:
                        new_actual_num = multiply_function(actual_num)
                        actual_num = new_actual_num
                        break
                    elif user_choice == 4:
                        new_actual_num = divide_function(actual_num)
                        actual_num = new_actual_num
                        break
                    elif user_choice == 5:
                        new_actual_num = delete_actual_number()
                        actual_num = new_actual_num
                        break
                    elif user_choice == 6:
                        exit_calculator(actual_num)
                else:
                    print('-----------------------')
                    print('the number you choose is not in the menu')
                    user_choice = input('Enter the number of your choice between 1 and 6: ')
                
            except ValueError:
                print('-----------------------')
                print('you must enter a number')
                user_choice = input('Enter the number of your choice: ')


###############  Operation functions
def sum_function(actual_num):
    user_num = input('Enter a number: ')
    checked_number = check_number_valid(user_num)

    new_num = actual_num + checked_number
    print('-----------------------')
    print(f'total number: {new_num}')
    print('-----------------------')
    return new_num


def subtract_function(actual_num):
    user_num = input('Enter a number: ')
    checked_number = check_number_valid(user_num)
    
    new_num = actual_num - checked_number
    print('-----------------------')
    print(f'total number: {new_num}')
    print('-----------------------')
    return new_num


def multiply_function(actual_num):
    user_num = input('Enter a number: ')
    checked_number = check_number_valid(user_num)

    new_num = actual_num * checked_number
    print('-----------------------')
    print(f'total number: {new_num}')
    print('-----------------------')
    return new_num


def divide_function(actual_num):
    user_num = input('Enter a number: ')
    checked_number = check_number_valid(user_num)
    while True:
        if checked_number != 0:
            break
        else: 
            print('-----------------------')
            print('Cannot divide by zero')
            user_num = input('Enter another number: ')
            checked_number = check_number_valid(user_num)

        
    new_num = actual_num / checked_number

    print('-----------------------')
    print(f'total number: {new_num}')
    print('-----------------------')
    return new_num


# Delete actual number function
def delete_actual_number():
    new_num = 0
    print('-----------------------')
    print(f'total number: {new_num}')
    print('-----------------------')
    return new_num


#Exit the calculator function
def exit_calculator(actual_num):
    print('-----------------------')
    print('Goodbye!')
    print(f'final result: {actual_num}')
    print('-----------------------')
    exit()


# check if the user input is a number
def check_number_valid(user_num):
    while True:
        try:
            user_num = int(user_num)
            break

        except:
            print('-----------------------')
            print('Please enter a number')
            user_num = input('Enter a new number: ')
    return user_num


def main():
    print('Welcome to the CLI calculator!!!!')
    try:
        initialize_calculator()
    
    except Exception as error:
        print('An error occurred. Please try again.')
        print(error)


if __name__ == "__main__":
    main()
