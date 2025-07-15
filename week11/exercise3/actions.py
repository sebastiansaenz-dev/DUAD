
# get student information function (option 1 form the menu)

class Student:
    def __init__(self, name, section, spanish_grade, english_grade, social_studies_grade, science_grade):
        self.name = name
        self.section = section
        self.spanish_grade = spanish_grade
        self.english_grade = english_grade
        self.social_studies_grade = social_studies_grade
        self.science_grade = science_grade

    def calculate_average(self):
        return (float(self.spanish_grade) + float(self.english_grade) + float(self.social_studies_grade) + float(self.science_grade)) / 4

def get_student_information():
    students = []
    while True:
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

            students.append(Student(valid_name, valid_section, valid_spanish_grade, valid_english_grade, valid_social_studies_grade, valid_science_grade))

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
        print(f'name: {student.name}')
        print(f'section: {student.section}')
        print(f'spanish grade: {student.spanish_grade}')
        print(f'english grade: {student.english_grade}')
        print(f'social studies grade: {student.social_studies_grade}')
        print(f'science grade: {student.science_grade}')
    print('------------------------')

#see top 3 best averages
def see_top_3_best_average(students):

    sorted_list = sorted(students, key=lambda student: student.calculate_average(), reverse=True)
    best_averages = sorted_list[:3]
    counter = 1
    print('------------------------')
    for student in best_averages:
        print(f'top {counter}: {student.name} with an average of {student.calculate_average():.2f}')
        counter += 1
    print('------------------------')

#see averages of all students
def see_students_average(students):
    total_students = len(students)
    averages = []
    for student in students:
        averages.append(student.calculate_average())

    total_sum = 0

    for average in averages:
        total_sum += average
    
    total_average = total_sum / total_students
    print('------------------------')
    print(f'the average all students is: {total_average:.2f}')
    print('------------------------')


########################################


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
                print('non-exported students are still here')
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