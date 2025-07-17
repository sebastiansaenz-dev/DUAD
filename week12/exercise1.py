


class BankAccount():
    def __init__(self):
        self._balance = 0


    def add_money(self, amount):
        self._balance += amount
        print(f'balance is: {self._balance}')
        return self._balance


    def remove_money(self, amount):
        while True:
            try:
                amount = int(amount)
                if self._balance >= amount:
                    self._balance -= amount
                    break
                else:
                    print('the amount is greater than the balance')
                    amount = int(input('please enter a valid amount: '))
            except ValueError:
                print('invalid amount')
                amount = input('please enter a valid amount: ')
        print(f'final balance is :{self._balance}')
        return self._balance

    def get_future_balance(self, amount):
        future_balance = self._balance - amount
        return future_balance


class SavingsAccount(BankAccount):
    def __init__(self, min_balance):
        self.min_balance = min_balance
        super().__init__()
    
    def remove_money(self, amount):
        try:
            if self.get_future_balance(amount) < self.min_balance:
                raise
            else:
                super().remove_money(amount)
                
        except:
            print("this will go below the account's minimum balance")
            print(f'final balance is :{self._balance}')



#put the minimum balance
my_account = SavingsAccount(500)

#add money to the bank account
my_account.add_money(1000)

#remove money from the bank account
my_account.remove_money(501)