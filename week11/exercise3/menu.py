

# actions functions
from actions import get_valid_menu_option
from actions import get_student_information
from actions import see_students_info
from actions import see_top_3_best_average
from actions import see_students_average
from actions import check_if_students_list_empty
from actions import check_students_info_empty
#data functions
from data import create_csv_file
from data import import_csv_file
from data import modify_csv_file
from data import check_file_exists
from data import convert_csv_to_objects
from data import convert_objects_to_dicts

def show_menu():
    students_info = []
    while True:
        print('1 to enter the information of a student')
        print('2 to see the information of all students')
        print('3 to see the top 3 students with best average')
        print('4 to see the average of each student')
        print('5 to export the information of all students to a csv file')
        print('6 to import the information of all students from a previous csv file')
        print('7 to clear the current non-exported student list')
        print('8 to exit the program')
        while True:
            user_choice = input('enter the number of your choice: ')
            try:
                user_choice = get_valid_menu_option(user_choice)
                break
            except Exception:
                print('an error has occurred, please enter a valid number')
        select_menu_option(user_choice, students_info)


def select_menu_option(user_choice, students_info):
    if user_choice == 1:
        new_student_info = get_student_information()
        students_info.extend(new_student_info)
    elif user_choice == 2:
        if check_if_students_list_empty(students_info):
            see_students_info(students_info)
        else:
            print('------------------------')
            print('there is no students in the list')
            print('------------------------')        
    elif user_choice == 3:
        if check_if_students_list_empty(students_info):
            see_top_3_best_average(students_info)
        else:
            print('------------------------')
            print('there is no students in the list')
            print('------------------------')
    elif user_choice == 4:
        if check_if_students_list_empty(students_info):
            see_students_average(students_info)
        else:
            print('------------------------')
            print('there is no students in the list')
            print('------------------------')         
    elif user_choice == 5:
        if students_info != []:
            if check_file_exists('students.csv'):
                converted_students_info = convert_objects_to_dicts(students_info)
                modify_csv_file('students.csv', converted_students_info, converted_students_info[0].keys())
                print('------------------------')  
                print('students information has been exported to a csv file')
                print('------------------------')  
                students_info.clear()
            else:
                converted_students_info = convert_objects_to_dicts(students_info)
                create_csv_file('students.csv', converted_students_info, converted_students_info[0].keys())
                print('------------------------')  
                print('students information has been exported to a csv file')
                print('------------------------')  
                students_info.clear()
        else:
            print('------------------------')
            print('there is no students in the list')
            print('------------------------')
    elif user_choice == 6:
        if check_file_exists('students.csv'):
            result = check_students_info_empty(students_info)
            if result == True:
                students_info.clear()
                imported_list = import_csv_file('students.csv')
                converted_list = convert_csv_to_objects(imported_list)
                students_info.extend(converted_list)
            elif result == 'import':
                imported_list = import_csv_file('students.csv')
                converted_list = convert_csv_to_objects(imported_list)
                students_info.extend(converted_list)
        else:
            print('------------------------')
            print('there is no file to import')
            print('------------------------')
    elif user_choice == 7:
        students_info.clear()
        print('------------------------')
        print('the list was cleared correctly!')
        print('------------------------')
    elif user_choice == 8:
        print('goodbye')
        exit()
