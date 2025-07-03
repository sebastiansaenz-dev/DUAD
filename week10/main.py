

from menu import show_menu, select_menu_option


def main():
    try:
        user_choice = show_menu()
        select_menu_option(user_choice)
    except Exception as error:
        print(error)
        print('there was an error')



if __name__ == "__main__":
    main()