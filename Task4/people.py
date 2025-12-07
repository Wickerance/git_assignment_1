# OOP Students
class Person:
    def __init__(self, fio, age):
        self.fio = fio
        self.age = age

    def display_info(self):
        print(f"ФИО: {self.fio}, Возраст: {self.age}")
        
    def get_scholarship(self):
        raise NotImplementedError("Метод стипендии должен быть реализован.")
        
    def is_scholarship_greater(self, other):
        # Сравнение размера стипендии
        return self.get_scholarship() > other.get_scholarship()

class Student(Person):
    # Номер группы, средний балл
    def __init__(self, fio, age, group_num, avg_grade):
        super().__init__(fio, age)
        self.group_num = group_num
        self.avg_grade = avg_grade
        
    def display_info(self):
        super().display_info()
        print(f"Группа: {self.group_num}, Средний балл: {self.avg_grade}")

    def get_scholarship(self):
        # Стипендия для студента
        if self.avg_grade == 5:
            return 6000
        elif self.avg_grade < 5 and self.avg_grade >= 4:
            return 4000
        return 0

class Aspirant(Student):
    # Научная работа
    def __init__(self, fio, age, group_num, avg_grade, research_title):
        super().__init__(fio, age, group_num, avg_grade)
        self.research_title = research_title

    def display_info(self):
        super().display_info()
        print(f"Научная работа: {self.research_title}")

    def get_scholarship(self):
        # Стипендия для аспиранта
        if self.avg_grade == 5:
            return 8000
        elif self.avg_grade < 5 and self.avg_grade >= 4:
            return 6000
        return 0

# Тестирование
if __name__ == '__main__':
    print("--- Тестирование Студентов ---")
    
    # Студенты
    s1 = Student("Иванов И.И.", 20, "201", 5.0) # 6000р
    s2 = Student("Петров П.П.", 20, "201", 4.0) # 4000р
    s3 = Student("Сидоров С.С.", 21, "201", 3.0) # 0р
    
    # Аспиранты
    a1 = Aspirant("Михайлов М.М.", 25, "101", 5.0, "Исследование 5.0") # 8000р
    a2 = Aspirant("Сергеев С.С.", 26, "101", 4.5, "Исследование 4.5") # 6000р

    s1.display_info()
    print(f"Стипендия (Студент 5.0): {s1.get_scholarship()}р")
    print(f"Стипендия (Студент 4.0): {s2.get_scholarship()}р")
    print(f"Стипендия (Студент 3.0): {s3.get_scholarship()}р")
    
    print("-" * 20)
    a1.display_info()
    print(f"Стипендия (Аспирант 5.0): {a1.get_scholarship()}р")
    print(f"Стипендия (Аспирант 4.5): {a2.get_scholarship()}р")
    
    print("-" * 20)
    # Тест сравнения
    print(f"Аспирант 5.0 > Студент 5.0 (по стипендии)? {a1.is_scholarship_greater(s1)}") # 8000 > 6000 -> True
    print(f"Студент 5.0 > Студент 3.0 (по стипендии)? {s1.is_scholarship_greater(s3)}") # 6000 > 0 -> True