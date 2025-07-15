
from abc import ABC, abstractmethod
from math import pi

class Shape(ABC):

    @abstractmethod
    def calculate_perimeter(self):
        pass


    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius


    def calculate_perimeter(self):
        return 2 * pi * self.radius
    

    def calculate_area(self):
        return pi * (self.radius ** 2)


class Square(Shape):
    def __init__(self, side):
        self.side = side
    

    def calculate_perimeter(self):
        return 4 * self.side
    

    def calculate_area(self):
        return self.side ** 2


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)
    

    def calculate_area(self):
        return self.length * self.width



my_circle = Circle(5)
print(f'perimeter of the circle: {my_circle.calculate_perimeter()}')
print(f'area of the circle: {my_circle.calculate_area()}')

my_square = Square(4)
print(f'perimeter of the square: {my_square.calculate_perimeter()}')
print(f'area of the square: {my_square.calculate_area()}')

my_rectangle = Rectangle(5, 7)
print(f'perimeter of the rectangle: {my_rectangle.calculate_perimeter()}')
print(f'area of the rectangle: {my_rectangle.calculate_area()}') 