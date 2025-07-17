
from datetime import date

def check_is_adult(func):
    def wrapper(user, *args):
        try:
            if user.age >= 18:
                print('this user is an adult')
            else:
                raise
        except Exception:
            print('this user is not and adult')
        
    return wrapper


class User:
    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth
    
    @property
    def age(self):
        today = date.today()
        return ((today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))))


my_user = User(date(2015, 1, 1))
print(f'age: {my_user.age}')


@check_is_adult
def only_adults_entry(user):
    pass

only_adults_entry(my_user)