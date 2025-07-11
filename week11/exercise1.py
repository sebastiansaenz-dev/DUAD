import math

class Circle:
    def __init__(self):
        self.radius = 20

    def get_area(self):
        area = math.pi * self.radius ** 2
        return area
    

new_circle = Circle()
print(new_circle.radius)
print(new_circle.get_area())
