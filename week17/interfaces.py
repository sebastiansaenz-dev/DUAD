

#type: ignore
import FreeSimpleGUI as sg

# imports from actions module
from actions import is_valid_string, is_valid_int

import services



# CATEGORY

def category_window():


    layout = [
        [sg.Text('Category name')],
        [sg.Input(key='-CATEGORY-')],
        [sg.Text('Category description')],
        [sg.Input(key='-CATEGORY_DESCRIPTION-')],
        [sg.Button('Create category')],
    ]

    window = sg.Window('Add Category', layout)


    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Create category':
            if is_valid_string(values['-CATEGORY-']) and is_valid_string(values['-CATEGORY_DESCRIPTION-']) and values['-CATEGORY-'] != '':
                services.create_category(values['-CATEGORY-'], values['-CATEGORY_DESCRIPTION-'])
                sg.popup(f"Category '{values['-CATEGORY-']}' created!")

            else:
                sg.popup("the category must be a string and can't be empty")
            
    window.close()


# EXPENSE WINDOW

def add_expense_window():

    categories = services.get_categories()
    categories_names = [category.name for category in categories]
    categories_names.append(' ')

    layout = [
        [sg.Text('Expense name')],
        [sg.Input(key='-EXPENSE_NAME-')],
        [sg.Text('Expense amount')],
        [sg.Input(key='-EXPENSE_AMOUNT-')],
        [sg.OptionMenu(categories_names, default_value=' ', key='-CATEGORY-')],
        [sg.Button('add expense')]
    ]

    window = sg.Window('Add Expense', layout)

    while True:
        event, values = window.read()


        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'add expense':
            if is_valid_string(values['-EXPENSE_NAME-']) and is_valid_int(values['-EXPENSE_AMOUNT-']) and values['-CATEGORY-'] != ' ' and values['-EXPENSE_AMOUNT-'] != '':

                services.create_transaction(
                    'expense',
                    values['-EXPENSE_NAME-'],
                    values['-CATEGORY-'],
                    values['-EXPENSE_AMOUNT-']
                )
                sg.popup('Expense added')

            else:
                sg.popup('the name, amount and category of the income cant be empty')
    
    window.close()



# INCOME WINDOW

def add_income_window():
    categories = services.get_categories()
    categories_names = [category.name for category in categories]
    categories_names.append(' ')

    layout = [
        [sg.Text('Income name')],
        [sg.Input(key='-INCOME_NAME-')],
        [sg.Text('Income amount')],
        [sg.Input(key='-INCOME_AMOUNT-')],
        [sg.OptionMenu(categories_names, default_value=' ', key='-CATEGORY-')],
        [sg.Button('add income')]
    ]

    window = sg.Window('Add income', layout)

    while True:
        event, values = window.read()


        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'add income':

            if is_valid_string(values['-INCOME_NAME-']) and is_valid_int(values['-INCOME_AMOUNT-']) and values['-INCOME_AMOUNT-'] != '' and values['-CATEGORY-'] != ' ':

                services.create_transaction(
                    'income',
                    values['-INCOME_NAME-'],
                    values['-CATEGORY-'],
                    values['-INCOME_AMOUNT-']
                )
                sg.popup('income added!')
                
            else:
                sg.popup('the name, amount and category of the income cant be empty')
    
    window.close()


# PRINCIPAL MENU WINDOW

def show_principal_menu():


    categories = services.get_categories()
    transactions = services.get_transactions()
    transactions_table = services.transactions_to_table_rows(transactions)

    categories_names = [category.name for category in categories]
    categories_names.append(' ')
    selected_transactions = []

    categories_table = services.categories_to_table_rows(categories)


    tap1_layout = [
        [sg.Text("Welcome to your personal finance manager")],
        [sg.Text("Transactions")],
        [sg.Table(transactions_table, headings=['type', 'name', 'category', 'amount'], key='-TABLE-')],
        [sg.Button('Add category'), sg.Button('Add expense'), sg.Button('Add income')],
        ]
    
    tap2_layout = [
        [sg.Text('Search for transactions')],
        [sg.Text('write the name of the transaction you want to search')],
        [sg.Input(key='-TRANSACTION_NAME-')],
        [sg.Text('Select the category of the transaction you want to search')],
        [sg.OptionMenu(categories_names, default_value=' ', key='-CATEGORY-')],
        [sg.Button('Search transaction')],
        [sg.Table(selected_transactions, headings=['type', 'name', 'category', 'amount'], key='-SELECTED_TRANSACTIONS_TABLE-')],
        [sg.Button('Delete transaction')],
    ]

    tap3_layout = [
        [sg.Text('Select the category you want to delete')],
        [sg.Table(categories_table, headings=['Name', 'Description'], key='-SELECTED_CATEGORY_TABLE-')],
        [sg.Button('Delete category')],
    ]

    layout = [[sg.TabGroup([[sg.Tab("Menu", tap1_layout), sg.Tab("Search transaction", tap2_layout), sg.Tab('Delete category', tap3_layout)]])]]
    window = sg.Window('Personal Finance Manager', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Add category':

            category_window()
            categories = services.get_categories()
            categories_names = [category.name for category in categories]
            categories_names.append(' ')
            window['-CATEGORY-'].update(values=categories_names, value=' ')

        elif event == 'Add expense':
            add_expense_window()
            transactions = services.get_transactions()
            window['-TABLE-'].update(values=services.transactions_to_table_rows(transactions))

        elif event == 'Add income':
            add_income_window()
            transactions = services.get_transactions()
            window['-TABLE-'].update(values=services.transactions_to_table_rows(transactions))

        elif event == 'Search transaction':
            selected_transactions = services.search_transactions(
                services.get_transactions(),
                values['-TRANSACTION_NAME-'],
                values['-CATEGORY-']
            )
            window['-SELECTED_TRANSACTIONS_TABLE-'].update(values=services.transactions_to_table_rows(selected_transactions))

        elif event == 'Delete transaction':

            if values['-SELECTED_TRANSACTIONS_TABLE-'] and selected_transactions:
                selected_index = values['-SELECTED_TRANSACTIONS_TABLE-'][0]
                transaction_to_delete = selected_transactions[selected_index]
                services.delete_transaction(transaction_to_delete)
                selected_transactions.pop(selected_index)
                window['-SELECTED_TRANSACTIONS_TABLE-'].update(
                    values=services.transactions_to_table_rows(selected_transactions))
                transactions = services.get_transactions()
                window['-TABLE-'].update(values=services.transactions_to_table_rows(transactions))
            
            else:
                sg.popup("Please select a transaction to delete.")
            
        elif event == 'Delete category':

            if values['-SELECTED_CATEGORY_TABLE-']:
                yes_no = sg.popup_yes_no("If you delete this category, all transactions assigned to it will also be deleted")
                if yes_no == 'Yes':
                    selected_index = values['-SELECTED_CATEGORY_TABLE-'][0]
                    category_to_delete = categories[selected_index]
                    services.delete_category(category_to_delete)
                    categories.pop(selected_index)
                    window['-SELECTED_CATEGORY_TABLE-'].update(
                        values=services.categories_to_table_rows(categories))
                    window['-CATEGORY-'].update(values=[c.name for c in categories])

                    transactions = services.get_transactions()
                    transactions_table = services.transactions_to_table_rows(transactions)
                    window['-TABLE-'].update(values=transactions_table)
            else:
                sg.popup('Please select a category to delete')
                    



    window.close()
