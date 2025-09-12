
from models import Category, Transaction

from data import add_unique_item, import_data, save_json


# EXPORT

def export_category(name, description, path='./categories.json'):

    categories = import_data(path)
    new_category = Category(name, description)
    update_list = add_unique_item(new_category.convert_to_dic(), categories)
    save_json(update_list, path)


def export_transaction(type, name, category, amount, path='./transactions.json'):

    transactions = import_data(path)
    new_transaction = Transaction(type, name, category, amount)
    update_list = add_unique_item(new_transaction.convert_to_dic(), transactions)
    save_json(update_list, path)


# SEARCH

def search_transactions(transactions, item_name, item_category):
    return [t for t in transactions if (item_name and t.name == item_name) or (item_category and t.category.name == item_category)]


# REMOVE TRANSACTION

def remove_transaction(transactions, transaction_to_remove):
    return [t for t in transactions if t != transaction_to_remove]

def search_transaction_to_delete(transaction_to_delete, path='./transactions.json'):
    transactions = import_data(path)
    transactions = [
        t for t in transactions
        if not (
            t['type'] == transaction_to_delete[0] and
            t['name'] == transaction_to_delete[1] and
            t['category'] == transaction_to_delete[2] and
            t['amount'] == transaction_to_delete[3]
        )
    ]
    save_json(transactions, path)
    return transactions

def remove_transactions_from_category(transactions, category):
    return [t for t in transactions if t.category.name != category.name]

def remove_category(categories, category_to_remove):
    return [c for c in categories if c != category_to_remove]

# CONVERT DATA TO INSTANCES

def convert_transactions_to_instances():
    categories = import_data('./categories.json')
    list_of_categories = [Category.convert_from_dic(c) for c in categories]
    
    transactions = import_data('./transactions.json')
    list_of_transactions = [Transaction.convert_from_dic(t, list_of_categories) for t in transactions]

    return list_of_transactions


def convert_categories_to_instances():
    categories = import_data('./categories.json')
    list_of_categories = [Category.convert_from_dic(c) for c in categories]

    return list_of_categories
