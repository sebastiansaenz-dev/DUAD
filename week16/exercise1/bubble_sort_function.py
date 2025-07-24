

def bubble_sort(list):
    for outer_index in range(0, len(list) - 1):
        has_made_changes = False
        for index in range(0, len(list) - 1 - outer_index):
            current_index = list[index]
            next_index = list[index + 1]

            if current_index > next_index:
                list[index] = next_index
                list[index + 1] = current_index
                has_made_changes = True

            print(f'this is the current index: {current_index} and the next index: {next_index}')

        if not has_made_changes:
            return list
    return list
