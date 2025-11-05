# Time Decorator
import time
import functools
import os

def initialize_input_file(filename="input.txt"):
    """Создает или перезаписывает файл input.txt с чистыми данными."""
    # Используем 'w' для перезаписи, явная кодировка utf-8
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("5\n7\n")
        # print(f"Файл {filename} инициализирован.")
    except Exception as e:
        print(f"Ошибка при инициализации файла {filename}: {e}")

def time_it(func):
    """Декоратор для вывода времени выполнения функции."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # Вывод времени выполнения функции
        print(f"Функция {func.__name__} выполнена за {end_time - start_time:.4f} сек.")
        return result
    return wrapper

@time_it
def sum_two_numbers(a, b):
    # Функция, вычисляющая сумму двух чисел
    result = a + b
    print(f"Результат сложения: {result}")
    return result

@time_it
def file_operation_task(input_file, output_file):
    # Функция, считывающая числа, вычисляющая сумму и записывающая результат в файл
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Читаем все содержимое и разделяем по пробелам/переносам строк
            content = f.read().split() 
        
        # Считываем и преобразуем два числа
        a = int(content[0])
        b = int(content[1])
        result = a + b

        # Запись результата в output.txt
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Сумма чисел из {input_file}: {result}")
        
        print(f"Результат записан в файл {output_file}")
        return result
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
        return None
    except (IndexError, ValueError):
        print(f"Ошибка: Не удалось считать два числа из файла {input_file}. Проверьте содержимое.")
        return None


# Тестирование
if __name__ == '__main__':
    initialize_input_file("input.txt") # 每次运行前确保文件干净
    print("--- Тестирование Декоратора ---")
    
    # 1. Функция с выводом суммы в консоль
    sum_two_numbers(5, 7)
    
    print("-" * 20)
    
    # 2. 函数 с чтением/записью файла
    file_operation_task("input.txt", "output.txt")