


from data import save_json

from logic import export_category
from logic import export_transaction
from logic import search_transactions
from logic import remove_transaction
from logic import convert_transactions_to_instances
from logic import convert_categories_to_instances
from logic import remove_transactions_from_category
from logic import remove_category


# CATEGORIES 

def create_category(name, description):
    export_category(name, description)


def get_categories():
    return convert_categories_to_instances()


# TRANSACTIONS

def create_transaction(type, name, category, amount):
    categories = get_categories()
    category_obj = next(c for c in categories if c.name == category)
    export_transaction(type, name, category_obj, amount)


def get_transactions():
    return convert_transactions_to_instances()


def find_transactions(name=None, category=None):
    transactions = get_transactions()
    return search_transactions(transactions, name, category)


def delete_transaction(transaction_to_remove):
    transactions = get_transactions()
    update_list = remove_transaction(transactions, transaction_to_remove)
    update_list_dicts = [t.convert_to_dic() for t in update_list]
    save_json(update_list_dicts, './transactions.json')
    return update_list_dicts


def transactions_to_table_rows(transactions):
    return [[t.type, t.name, t.category.name, t.amount] for t in transactions]

def categories_to_table_rows(categories):
    return [[c.name, c.description] for c in categories]


def delete_category(category_to_remove):
    transactions = get_transactions()
    update_list = remove_transactions_from_category(transactions, category_to_remove)
    update_list_dicts = [t.convert_to_dic() for t in update_list]
    save_json(update_list_dicts, './transactions.json')

    categories = get_categories()
    update_category_list = remove_category(categories, category_to_remove)
    update_category_list_dicts = [c.convert_to_dic() for c in update_category_list]
    save_json(update_category_list_dicts, './categories.json')


