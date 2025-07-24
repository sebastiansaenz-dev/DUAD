def bubble_sort(list): # O(n^2)
    for outer_index in range(0, len(list) - 1): # O(n)
        has_made_changes = False # O(1)
        for index in range(0, len(list) - 1 - outer_index): # O(n)
            current_index = list[index] # O1)
            next_index = list[index + 1] # O(1)

            if current_index > next_index: # O(1)
                list[index] = next_index # O(1)
                list[index + 1] = current_index # O(1)
                has_made_changes = True # O(1)

            print(f'this is the current index: {current_index} and the next index: {next_index}') # O(1)

        if not has_made_changes: # O(1)
            return # O(1)