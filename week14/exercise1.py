

class Node:
    data: str
    next: 'Node'

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Stack:
    top: Node

    def __init__(self, top):
        self.top = top


    def print_structure(self):
        current_node = self.top

        while (current_node is not None):
            print(current_node.data)
            current_node = current_node.next


    def push(self, new_node):
        new_node.next = self.top
        self.top = new_node
    

    def pop(self):
        if self.top:
            self.top = self.top.next


first_node = Node('primero')
my_stack = Stack(first_node)

second_node = Node('segundo')
my_stack.push(second_node)

third_node = Node('third')
my_stack.push(third_node)


my_stack.print_structure()


print('pop down here')

my_stack.pop()

my_stack.print_structure()