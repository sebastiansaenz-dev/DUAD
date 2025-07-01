
import csv
import os

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
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
