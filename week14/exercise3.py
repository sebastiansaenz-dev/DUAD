

class Node:
    data: str
    left: 'Node'
    right: 'Node'
    
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinaryTree:
    root: Node

    def __init__(self, root):
        self.root = root


    def print_tree(self, node):
        if node is not None:
            self.print_tree(node.left)
            print(node.data)
            self.print_tree(node.right)



first_node = Node('first')
my_binary_tree = BinaryTree(first_node)

second_node = Node('second')
third_node = Node('third')
fourth_node = Node('fourth')
fifth_node = Node('fifth')
sixth_node = Node('sixth')
seventh_node = Node('seventh')

first_node.left = second_node
first_node.right = third_node
second_node.left = fourth_node
second_node.right = fifth_node
third_node.left = sixth_node
third_node.right = seventh_node

my_binary_tree.print_tree(my_binary_tree.root)  