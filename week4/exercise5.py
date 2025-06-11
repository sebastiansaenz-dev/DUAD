#Exercise 5

number_grades = int(input("enter number of grades: "))

grade = 0
number_approved_grades = 0
number_failed_grades = 0
total_grades_approved = 0
total_failed_grades = 0
total_grades = 0

counter = 0

while (counter < number_grades):
    grade = int(input("enter grade: "))
    if (grade >= 70):
        number_approved_grades += 1
        total_grades += grade
        total_grades_approved += grade
    else:
        number_failed_grades += 1
        total_grades += grade
        total_failed_grades += grade
    counter += 1

if (number_failed_grades == 0):
    average_of_approved_grades = total_grades_approved / number_approved_grades
    total_average = total_grades / number_grades
    print(f'number od approved grades: {number_approved_grades}')
    print(f'average of approved grades: {average_of_approved_grades}')
    print(f'average of all grades: {total_average}')
elif (number_approved_grades == 0):
    average_of_failed_grades = total_failed_grades / number_failed_grades
    total_average = total_grades / number_grades
    print(f'number of failed grades: {number_failed_grades}')
    print(f'average of failed grades: {average_of_failed_grades}')
    print(f'average of all grades: {total_average}')
else:
    average_of_approved_grades = total_grades_approved / number_approved_grades
    average_of_failed_grades = total_failed_grades / number_failed_grades
    total_average = total_grades / number_grades
    print(f'number of approved grades: {number_approved_grades}')
    print(f'number of failed grades: {number_failed_grades}')
    print(f'average of approved grades is {average_of_approved_grades}')
    print(f'average of failed grades is {average_of_failed_grades}')
    print(f'average of all grades is {total_average}')