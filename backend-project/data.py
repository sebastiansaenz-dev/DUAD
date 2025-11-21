
import json
import os

def check_if_exists(key, value, item_list):
    return any(item[key] == value for item in item_list)


def check_if_file_exist(path):
    if not os.path.exists(path):
        with open(path, "w") as file:
            json.dump([], file)


def import_data(path):
    with open(path) as file:
        data = file.read().strip()
        return json.loads(data) if data else []


def export_data(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def add_item_to_list(new_item, actual_list):
    actual_list.append(new_item)
    return actual_list


def add_to_json(new_data, actual_list):
    actual_list.append(new_data)
    return actual_list

