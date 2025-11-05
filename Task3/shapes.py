# OOP Shapes
import math

class Shape:
    # Базовый класс для геометрических фигур
    def area(self):
        raise NotImplementedError("Метод площади должен быть реализован.")
    
    def perimeter(self):
        raise NotImplementedError("Метод периметра должен быть реализован.")
        
    def is_area_greater(self, other):
        return self.area() > other.area()

    def is_perimeter_greater(self, other):
        return self.perimeter() > other.perimeter()

class Circle(Shape):
    def __init__(self, radius):
        self.r = radius
        
    def area(self):
        return math.pi * self.r ** 2
        
    def perimeter(self):
        return 2 * math.pi * self.r

class Rectangle(Shape):
    def __init__(self, width, height):
        self.w = width
        self.h = height
        
    def area(self):
        return self.w * self.h
        
    def perimeter(self):
        return 2 * (self.w + self.h)

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side) # Наследует от Rectangle

class Triangle(Shape):
    # Используем 3 стороны для формулы Герона
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def area(self):
        s = self.perimeter() / 2 # Полупериметр
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        
    def perimeter(self):
        return self.a + self.b + self.c

# Тестирование
if __name__ == '__main__':
    print("--- Тестирование фигур ---")
    r = Rectangle(5, 10)
    s = Square(6)
    c = Circle(4)
    t = Triangle(3, 4, 5) # Прямоугольный треугольник

    print(f"Прямоугольник: S={r.area():.2f}, P={r.perimeter():.2f}")
    print(f"Квадрат: S={s.area():.2f}, P={s.perimeter():.2f}")
    print(f"Круг: S={c.area():.2f}, P={c.perimeter():.2f}")
    print(f"Треугольник: S={t.area():.2f}, P={t.perimeter():.2f}")

    # Тестирование сравнения
    print(f"\nСравнение:")
    print(f"Квадрат > Прямоугольник (по площади)? {s.is_area_greater(r)}")
    print(f"Круг > Треугольник (по периметру)? {c.is_perimeter_greater(t)}")