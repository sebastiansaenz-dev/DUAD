
#type: ignore
import pytest
from models import Category, Transaction
from logic import search_transactions
from logic import remove_transactions_from_category
from logic import remove_transaction
from logic import remove_category
from actions import is_valid_string
from actions import is_valid_int


def test_search_transactions_by_name():
    #Arrange
    food = Category('food', '')
    home = Category('home', '')
    list_of_transactions = [
        Transaction('income', 'rent', home, 222),
        Transaction('expense', 'pizza', food, 444),
        Transaction('income', 'furniture', home, 4454)
    ]


    item_name = 'pizza'
    item_category = None
    #Act

    result = search_transactions(list_of_transactions, item_name, item_category)

    #Assert

    assert result[0].name == 'pizza'


def test_search_transactions_by_category():
    #Arrange
    food = Category('food', '')
    home = Category('home', '')
    list_of_transactions = [
        Transaction('income', 'rent', home, 222),
        Transaction('expense', 'pizza', food, 444),
        Transaction('income', 'furniture', home, 4454)
    ]


    item_name = None
    item_category = home.name
    #Act

    result = search_transactions(list_of_transactions, item_name, item_category)

    #Assert

    assert result[0].name == 'rent' and result[1].name == 'furniture'


def test_remove_transaction():
    #Arrange

    food = Category('food', '')
    home = Category('home', '')
    transactions = [
        Transaction('income', 'rent', home, 222),
        Transaction('expense', 'pizza', food, 444),
        Transaction('income', 'furniture', home, 4454)
    ]

    transaction_to_remove = Transaction('expense', 'pizza', food, 444)


    #Act
    result = remove_transaction(transactions, transaction_to_remove)


    #Assert
    assert result[0].name == 'rent' and result[1].name == 'furniture'


def test_remove_category():
    categories = [
        Category('food', 'description'),
        Category('rent', 'description'),
        Category('exercise', 'description'),
        Category('school', 'description')
    ]

    category_to_remove = Category('rent', 'description')

    result = remove_category(categories, category_to_remove)

    assert result[0].name == 'food' and result[1].name == 'exercise' and result[2].name == 'school'


def test_remove_transactions_from_category():
    food = Category('food', '')
    home = Category('home', '')
    
    transactions = [
        Transaction('income', 'rent', home, 222),
        Transaction('expense', 'pizza', food, 444),
        Transaction('income', 'furniture', home, 4454),
        Transaction('expense', 'windows', home, 9595)
    ]

    category = home


    result = remove_transactions_from_category(transactions, category)

    assert result[0].name == 'pizza'


def test_is_valid_string_with_string():
    #Arrange

    value = 'string'

    #Act
    result = is_valid_string(value)


    #Assert
    assert result == True


def test_is_valid_string_with_int():
    #Arrange

    value = 344

    #Act
    result = is_valid_string(value)


    #Assert
    assert result == False


def test_is_valid_string_with_spaces():
    value = ' '

    result = is_valid_string(value)

    assert result == False


def test_is_valid_int_with_int():
    value = 54

    result = is_valid_int(value)

    assert result == True


def test_is_valid_int_with_string():
    value = 'hello world'

    result = is_valid_int(value)

    assert result == False

