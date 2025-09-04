

import json
import os


def check_if_file_exists(file):
    if not os.path.exists(file):
        with open(file, 'w') as file:
            json.dump([], file)


def import_data(path):
    with open(path) as file:
        content = file.read().strip()
        return json.loads(content) if content else []


def add_unique_item(new_item, existing_list):
    if not any(item['name'] == new_item['name'] for item in existing_list):
        existing_list.append(new_item)
    return existing_list


def save_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

