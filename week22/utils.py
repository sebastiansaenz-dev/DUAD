

import csv
import os



def export_csv(file_path, data, headers):
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(data)


def check_if_folder_exists(path):
    os.makedirs(path, exist_ok=True)
    return True