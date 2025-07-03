
# get student information function (option 1 form the menu)

def get_student_information():
    students = []
    while True:
        temporal_dic = {}
        try:
            student_name = input("enter the student's name: ")
            valid_name = check_valid_string(student_name)

            student_section = input("enter the student's section: ")
            valid_section = check_valid_section(student_section)

            student_spanish_grade = input("enter the student's spanish grade: ")
            valid_spanish_grade = check_valid_grade(student_spanish_grade)
            
            student_english_grade = input("enter the student's english grade: ")
            valid_english_grade = check_valid_grade(student_english_grade)
            
            student_social_studies_grade = input("enter the student's social studies grade: ")
            valid_social_studies_grade = check_valid_grade(student_social_studies_grade)
            
            student_science_grade = input("enter the student's science grade: ")
            valid_science_grade = check_valid_grade(student_science_grade)
            
            temporal_dic['student_name'] = valid_name
            temporal_dic['section'] = valid_section
            temporal_dic['spanish_grade'] = valid_spanish_grade
            temporal_dic['english_grade'] = valid_english_grade
            temporal_dic['social_studies_grade'] = valid_social_studies_grade
            temporal_dic['science_grade'] = valid_science_grade

            students.append(temporal_dic)

            new_student_option = input('do you want to add another student? (yes/no): ')
            checked_new_student_option = check_yes_no_option(new_student_option)

            if checked_new_student_option == 'no':
                print('------------------------')
                print('the information has been saved')
                print('------------------------')
                break
            else:
                continue

        except Exception as error:
            print(error)
            print("invalid input, please try again")
    return students


#see the information of all students
def see_students_info(students):
    for student in students:
        print('------------------------')
        print(f'name: {student['student_name']}')
        print(f'section: {student["section"]}')
        print(f'spanish grade: {student["spanish_grade"]}')
        print(f'english grade: {student["english_grade"]}')
        print(f'social studies grade: {student["social_studies_grade"]}')
        print(f'science grade: {student["science_grade"]}')
    print('------------------------')

#see top 3 best averages
def see_top_3_best_average(students):
    students_average = calculate_average(students)

    students_average.sort(key=lambda student: student['average'], reverse=True)
    best_averages = students_average[:3]
    counter = 1
    print('------------------------')
    for average in best_averages:
        print(f'top {counter}: {average['student_name']} with an average of {average["average"]}')
        counter += 1
    print('------------------------')

#see averages of all students
def see_students_average(students):
    total_students = len(students)
    students_average = calculate_average(students)
    averages = []
    for student in students_average:
        averages.append(student['average'])

    total_sum = 0

    for average in averages:
        total_sum += average
    
    total_average = total_sum / total_students
    print('------------------------')
    print(f'the average all students is: {total_average}')
    print('------------------------')


########################################


def calculate_average(students):
    students_average = []
    for student in students:
        temporal_dic = {}
        student_name = student['student_name']
        spanish = float(student['spanish_grade'])
        english = float(student['english_grade'])
        social_studies = float(student['social_studies_grade'])
        science = float(student['science_grade'])
        average = (spanish + english + social_studies + science) / 4

        temporal_dic['student_name'] = student_name
        temporal_dic['average'] = average
        students_average.append(temporal_dic)
    return students_average

#check functions
def check_if_students_list_empty(students):
    if students != []:
        return True


def check_students_info_empty(students):
    if students != []:
        print('------------------------')
        print('there are students in the list waiting for being export to the csv file')
        user_choice = input('do you want to clear the new students from the list to import the students from de csv file? (yes/no): ')
        print('------------------------')
        while True:
            if user_choice.strip().lower() == 'yes':
                return True
            elif user_choice.strip().lower() == 'no':
                print('------------------------')
                print('non-exported students still here')
                print('------------------------')
                return False
            else:
                print('------------------------')
                print('you must enter yes or no')
                user_choice = input('do you want to clear the new students from the list to import the students from de csv file? (yes/no): ')
                print('------------------------')
    else:
        return 'import'

def check_yes_no_option(option):
    while True:
        try:
            option = str(option)
            user_option = option.strip().lower()
            if user_option.strip().lower() == "yes" or user_option.strip().lower() == "no":
                return user_option
            else:
                print("invalid option, please enter yes or no")
                option = input("do you want to add another student? (yes/no): ")
        except ValueError:
            print('invalid input, please enter yes or no')
            option = input('do you want to add another student? (yes/no): ')


def check_valid_grade(grade):
    while True:
        try:
            grade = float(grade)
            if (grade >= 0 and grade <= 100):
                return grade
            else:
                print("grade must be between 0 and 100")
                grade = input("enter the grade: ")
        except ValueError:
            print('please enter a valid number')
            grade = input("enter the grade: ")


def check_valid_section(student_section):
    while True:
        try:
            digits_part = student_section[:-1]
            letter_part = student_section[-1]

            if digits_part.isdigit():
                digits_part = int(digits_part)
            else:
                print('invalid section, please enter a valid section (e.g. 1A)')
                student_section = input("enter the student's section: ")
                continue

            if digits_part < 1 or digits_part > 12:
                print("section number must be between 1 and 12")
                student_section = input("enter the student's section: ")
                continue

            if letter_part.isalpha():
                letter_part = str(student_section[-1])
                student_section = student_section[:-1] + letter_part.upper()
                return student_section
            else:
                print('invalid section, please enter a valid section (e.g. 1A)')
                student_section = input("enter the student's section: ")
                continue
            
        except ValueError:
            print('invalid section')
            student_section = input("enter the student's section: ")
            continue


def check_valid_number(num_to_check):
    while True:
        try:
            num_to_check = int(num_to_check)
            return num_to_check
        except ValueError:
            print('please enter a number')
            num_to_check = input('Enter a number: ')


def check_valid_string(user_input):
    while True:
        try:
            if not user_input.replace(' ', '').isalpha():
                print('please enter a string')
                user_input = input('Enter a string: ')
            else:
                return user_input
        except Exception:
            print('please enter a string')
            user_input = input('Enter a string: ')


def get_valid_menu_option(user_choice):
    while True:
        try:
            user_choice = int(user_choice)
            if user_choice >= 1 and user_choice <= 8:
                return user_choice
            else:
                print('you must enter a number between 1 and 8')
                user_choice = input('enter the number of your choice: ')
        except Exception as error:
            print('you must enter a integer')
            user_choice = input('enter the number between 1 and 8: ')