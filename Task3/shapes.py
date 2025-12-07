"""
Модуль, реализующий иерархию геометрических фигур.
"""
import math

class Shape:
    """Базовый класс для геометрических фигур."""
    
    def area(self):
        """Вычисляет площадь фигуры."""
        raise NotImplementedError("Метод площади должен быть реализован.")
    
    def perimeter(self):
        """Вычисляет периметр фигуры."""
        raise NotImplementedError("Метод периметра должен быть реализован.")
        
    def is_area_greater(self, other):
        """Сравнивает площадь с другой фигурой."""
        return self.area() > other.area()

    def is_perimeter_greater(self, other):
        """Сравнивает периметр с другой фигурой."""
        return self.perimeter() > other.perimeter()

class Circle(Shape):
    """Класс, описывающий круг."""
    
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return math.pi * self.radius ** 2
        
    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    """Класс, описывающий прямоугольник."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
        
    def perimeter(self):
        return 2 * (self.width + self.height)

class Square(Rectangle):
    """Класс, описывающий квадрат."""
    
    def __init__(self, side):
        super().__init__(side, side)  # Наследует от Rectangle

class Triangle(Shape):
    """Класс, описывающий треугольник."""
    
    def __init__(self, side_a, side_b, side_c):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        
    def area(self):
        # Используем формулу Герона
        semi_perimeter = self.perimeter() / 2
        return math.sqrt(
            semi_perimeter * (semi_perimeter - self.side_a) * (semi_perimeter - self.side_b) * (semi_perimeter - self.side_c)
        )
        
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c

# Тестирование
if __name__ == '__main__':
    print("--- Тестирование фигур ---")
    rectangle = Rectangle(5, 10)
    square = Square(6)
    circle = Circle(4)
    triangle = Triangle(3, 4, 5)  # Прямоугольный треугольник

    print(f"Прямоугольник: S={rectangle.area():.2f}, P={rectangle.perimeter():.2f}")
    print(f"Квадрат: S={square.area():.2f}, P={square.perimeter():.2f}")
    print(f"Круг: S={circle.area():.2f}, P={circle.perimeter():.2f}")
    print(f"Треугольник: S={triangle.area():.2f}, P={triangle.perimeter():.2f}")

    # Тестирование сравнения
    print(f"\nСравнение:")
    print(f"Квадрат > Прямоугольник (по площади)? {square.is_area_greater(rectangle)}")
    print(f"Круг > Треугольник (по периметру)? {circle.is_perimeter_greater(triangle)}")