class Node:
    data: int
    next: "Node"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    head: Node

    def __init__(self, head):
        self.head = head

    def print_structure(self):
        current_node = self.head

        while (current_node is not None):
            print(current_node.data)
            current_node = current_node.next
    

    def bubble_sort(self):
        has_made_changes = True
        current_node = self.head

        while has_made_changes:
            has_made_changes = False
            current_node = self.head
            previous_node = None

            while current_node and current_node.next:
                next_node = current_node.next

                if current_node.data > next_node.data:
                    if previous_node:
                        previous_node.next = next_node
                    else:
                        self.head = next_node
                    
                    current_node.next = next_node.next
                    next_node.next = current_node

                    previous_node = next_node
                    has_made_changes = True
                else:
                    previous_node = current_node
                    current_node = current_node.next


third_node = Node(1000)
second_node = Node(80000, third_node)
first_node = Node(92000, second_node)

linked_list = LinkedList(first_node)
linked_list.bubble_sort()
linked_list.print_structure()

