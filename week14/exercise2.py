

class Node:
    data: str
    next: 'Node'

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class DoubleEndedQueue:
    head: Node

    def __init__(self, head):
        self.head = head
        self.tail = head


    def print_structure(self):
        current_node = self.head

        while (current_node is not None):
            print(current_node.data)
            current_node = current_node.next
    

    def push_right(self, new_node):

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node


    def push_left(self, new_node):
        new_node.next = self.head
        self.head = new_node
        if self.tail is None:
            self.tail = new_node


    def pop_right(self):
        if self.head is None:
            return
        
        if self.head.next is None:
            self.head = None
            self.tail = None
            return

        current_node = self.head
        previous_node = None

        while (current_node.next is not None):
            previous_node = current_node
            current_node = current_node.next
            
        previous_node.next = None
        self.tail = previous_node


    def pop_left(self):
        if self.head:
            self.head = self.head.next


first_node = Node('primero')
my_double = DoubleEndedQueue(first_node)

second_node = Node('segundo')
my_double.push_left(second_node)

third_node = Node('third')
my_double.push_right(third_node)

my_double.print_structure()

print('--------------')
print('pops')
print('--------------')


my_double.pop_right()

my_double.print_structure()
