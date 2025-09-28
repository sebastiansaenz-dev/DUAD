
import json
import os


def is_homework_in_list(title, actual_list):
    return any(item['title'] == title for item in actual_list)
    


def check_if_file_exists(file):
    if not os.path.exists(file):
        with open(file, 'w') as file:
            json.dump([], file)


def check_valid_status(status):
    if status == 'not started' or status == 'on progress' or status == 'done':
        return True
    else:
        return False

def import_data(path):
    with open(path) as file:
        content = file.read().strip()
        return json.loads(content) if content else []


def add_homework(new_item, actual_list):
    actual_list.append(new_item)
    return actual_list


def export_data(data, path='./homeworks.json'):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
