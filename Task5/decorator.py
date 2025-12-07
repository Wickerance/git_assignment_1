"""
Модуль для демонстрации работы декораторов.
"""
import time
import functools

DEFAULT_INPUT_FILE = "input.txt"
DEFAULT_OUTPUT_FILE = "output.txt"

def initialize_input_file(filename=DEFAULT_INPUT_FILE):
    """Создает или перезаписывает файл с входными данными."""
    # Используем 'w' для перезаписи, явная кодировка utf-8
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("5\n7\n")
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
    """Функция, вычисляющая сумму двух чисел."""
    result = a + b
    print(f"Результат сложения: {result}")
    return result

@time_it
def file_operation_task(input_file, output_file):
    """Функция, считывающая числа из файла и записывающая сумму в другой файл."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Читаем все содержимое и разделяем по пробелам/переносам строк
            content = f.read().split() 
        
        if len(content) < 2:
            print(f"Ошибка: в файле {input_file} недостаточно данных.")
            return None

        # Считываем и преобразуем два числа
        num_a = int(content[0])
        num_b = int(content[1])
        result = num_a + num_b

        # Запись результата в выходной файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Сумма чисел из {input_file}: {result}")
        
        print(f"Результат записан в файл {output_file}")
        return result
        
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
        return None
    except (IndexError, ValueError) as e:
        print(f"Ошибка обработки данных: {e}")
        return None


# Тестирование
if __name__ == '__main__':
    initialize_input_file(DEFAULT_INPUT_FILE) # Очистка файла перед запуском
    print("--- Тестирование Декоратора ---")
    
    # 1. Функция с выводом суммы в консоль
    sum_two_numbers(5, 7)
    
    print("-" * 20)
    
    # 2. Функция с чтением/записью файла
    file_operation_task(DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE)