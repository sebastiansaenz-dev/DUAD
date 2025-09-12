
from interfaces import show_principal_menu
from data import check_if_file_exists


def main():

    check_if_file_exists('./transactions.json')
    check_if_file_exists('./categories.json')

    show_principal_menu()

if __name__ == "__main__":
    main()






