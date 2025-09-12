class Category:

    def __init__(self, name, description):
        self.name = name
        self.description = description

    
    def __eq__(self, other):
        if isinstance(other, Category):
            return (
                self.name == other.name and
                self.description == other.description
            )
        return False
    

    def convert_to_dic(self):
        dic = {}
        dic['name'] = self.name
        dic['description'] = self.description
        return dic


    def print_category(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")


    def print_category_expenses(list_expenses):
        for expense in list_expenses:
            print(expense.name)


    def print_category_incomes(list_incomes):
        for income in list_incomes:
            print(income.name)


    @classmethod
    def convert_from_dic(cls, dic):
        return cls(dic['name'], dic['description'])




class Transaction:
    def __init__(self, type, name, category, amount):
        self.type = type
        self.name = name
        self.category = category
        self.amount = amount


    def __eq__(self, other):
        if isinstance(other, Transaction):
            return (
                self.type == other.type and
                self.name == other.name and
                self.category.name == other.category.name and
                self.amount == other.amount
            )
        return False


    def print_expense(self):
        print(f'Type: {self.type}')
        print(f"Name: {self.name}")
        print(f'Category: {self.category.name}')
        print(f'Amount: {self.amount}')
    

    def convert_to_dic(self):
        dic = {}
        dic['type'] = self.type
        dic['name'] = self.name
        dic['category'] = self.category.name
        dic['amount'] = self.amount
        
        return dic
    

    @classmethod
    def convert_from_dic(cls, dic, categories):
        category_obj = next((category for category in categories if category.name == dic['category']), None)
        return cls(dic['type'], dic['name'], category_obj, dic['amount'])
    
