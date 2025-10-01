
from data import import_data
from data import add_homework
from data import export_data



def export_homework(new_homework,  path='./homeworks.json'):
    actual_homeworks = import_data(path)
    update_list = add_homework(new_homework, actual_homeworks)
    export_data(update_list, path)

def import_homeworks(path='./homeworks.json'):
    homeworks = import_data(path)
    return homeworks


