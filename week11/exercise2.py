

class Bus:
    max_passengers = 3
    passengers = []

    def add_passenger(self, person):
        self.passengers.append(person)
    
    def check_seats_available(self):
        if len(self.passengers) < self.max_passengers:
            return True
        else:
            print('------------------')
            print("Bus is full.")
            print('------------------')
            print()
            return False

    def remove_passenger(self):
        self.passengers.pop(0)


class Person:
    def __init__(self, name):
        self.name = name


def menu():
    while True:
        print('1: add passenger')
        print('2: remove passenger')
        print('3: exit the program')

        user_choice = input('enter your choice: ')
        checked_user_choice = get_valid_menu_option(user_choice)
        select_menu_option(checked_user_choice)


def select_menu_option(user_choice):
    bus = Bus()
    if user_choice == 1:
        board_passengers(bus)
    elif user_choice == 2:
        remove_passenger(bus)
    elif user_choice == 3:
        print('goodbye')
        exit()


def board_passengers(bus):
    while True:
        seats_available = bus.check_seats_available()
        if seats_available == False:
            break
        else:
            pass
        passenger_name = input("Enter passenger name: ")
        checked_passenger_name = check_valid_name(passenger_name)

        new_person = Person(checked_passenger_name)
        bus.add_passenger(new_person.name)
        user_choice = input("Do you want to add another passenger? (yes/no): ")
        check_user_choice = check_yes_no_option(user_choice)
        if check_user_choice == 'yes':
            continue
        elif check_user_choice == 'no':
            print('------------------')
            print(bus.passengers)
            print('------------------')
            break

def remove_passenger(bus):
    user_choice = input('want to remove passenger? (yes/no) ')
    checked_user_choice = check_yes_no_option(user_choice)
    if checked_user_choice == 'yes':
        bus.remove_passenger()
        print('------------------')
        print(bus.passengers)
        print('------------------')

    else:
        print('------------------')
        print(bus.passengers)
        print('------------------')


def get_valid_menu_option(user_choice):
    while True:
        try:
            user_choice = int(user_choice)
            if user_choice >= 1 and user_choice <= 3:
                return user_choice
            else:
                print('you must enter 1 or 3')
                user_choice = input('enter the number of your choice: ')
        except Exception as error:
            print('you must enter a integer')
            user_choice = input('enter the number 1 or 3: ')


def check_valid_name(user_input):
    while True:
        try:
            if user_input.isalpha():
                return user_input
            else:
                
                print("Invalid name. Please enter a valid name.")
                user_input = input("Enter passenger name: ")

        except Exception:
            print("Invalid name. Please enter a valid name.")
            user_input = input("Enter passenger name: ")


def check_yes_no_option(option):
    while True:
        try:
            option = str(option)
            user_option = option.strip().lower()
            if user_option.strip().lower() == "yes" or user_option.strip().lower() == "no":
                return user_option
            else:
                print("invalid option, please enter yes or no")
                option = input("do you want to remove a passenger? (yes/no): ")
        except ValueError:
            print('invalid input, please enter yes or no')
            option = input('do you want to remove a passenger? (yes/no): ')


def main():
    try:
        user_choice = menu()
        select_menu_option(user_choice)
    except Exception as error:
        print(error)
        print('there was an error')


if __name__ == "__main__":
    main()