
#Exercise 6

def sort_list(string):
    strings_list = string.split('-')
    strings_list.sort()
    return strings_list


def detect_empty_strings(list):
    for item in range(len(list) -1, -1, -1):
        if list[item] == '':
            list.pop(item)
    print(list)


my_string = input('enter a string of words separated by a hyphen: ')

detect_empty_strings(sort_list(my_string))