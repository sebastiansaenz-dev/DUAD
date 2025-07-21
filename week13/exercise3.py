
from datetime import date

def check_is_adult(func):
    def wrapper(user, *args):
        if user.age >= 18:
            print('this user is an adult')
            return func(user, *args)
        else:
            print('this user is not and adult')

    return wrapper


class User:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth
    
    @property
    def age(self):
        today = date.today()
        return ((today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))))

print('adult')
my_adult_user = User(date(1990, 1, 1))
print(f'age: {my_adult_user.age}')

@check_is_adult
def only_adults_entry(user):
    print('starting the entry process')

only_adults_entry(my_adult_user)

print('------------------')

print('not adult')
my_not_adult_user = User(date(2020, 1, 1))
print(f'age: {my_not_adult_user.age}')

only_adults_entry(my_not_adult_user)
