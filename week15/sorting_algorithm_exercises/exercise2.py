

def bubble_sort(list):
    for outer_index in range(0, len(list) - 1):
        has_made_changes = False
        for index in range(len(list) - 1 - outer_index, 0, -1):
            current_index = list[index]
            next_index = list[index - 1]

            if current_index < next_index:
                list[index] = next_index
                list[index - 1] = current_index
                has_made_changes = True

            print(f'this is the current index: {current_index} and the next index: {next_index}')

        if not has_made_changes:
            return



list_to_sort = [64, 34, 25, 12, 22, 11, 90]

bubble_sort(list_to_sort)

print(list_to_sort)