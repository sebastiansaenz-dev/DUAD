
import csv
import os
from actions import Student

def check_file_exists(file_path):
    return os.path.exists(file_path)


def create_csv_file(file_path, data, headers):
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(data)


def modify_csv_file(file_path, data, headers):
    with open(file_path, 'a', encoding='utf-8') as file:
        writer = csv.DictWriter(file, headers)
        writer.writerows(data)


def import_csv_file(path):
    new_list = []
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_list.append(row)
        print('------------------------')
        print('imported all students from csv file')
        print('------------------------')
        return new_list
            


def convert_csv_to_objects(list_of_students):
    new_students_list = []

    for student in list_of_students:
        name = student['student_name']
        section = student['section']
        spanish_grade = student['spanish_grade']
        english_grade = student['english_grade']
        social_studies_grade = student['social_studies_grade']
        science_grade = student['science_grade']

        new_students_list.append(Student(name, section, float(spanish_grade), float(english_grade), float(social_studies_grade), float(science_grade)))
    return new_students_list


def convert_objects_to_dicts(list_of_students):
    new_students_list = []

    for student in list_of_students:
        temporal_dic = {}
        temporal_dic['student_name'] = student.name
        temporal_dic['section'] = student.section
        temporal_dic['spanish_grade'] = float(student.spanish_grade)
        temporal_dic['english_grade'] = float(student.english_grade)
        temporal_dic['social_studies_grade'] = float(student.social_studies_grade)
        temporal_dic['science_grade'] = float(student.science_grade)

        new_students_list.append(temporal_dic)
    return new_students_list
