"""
Модуль для фильтрации массивов с использованием лямбда-функций.
"""

def filter_array(func, array):
    """
    Фильтрует массив на основе переданной функции.

    Args:
        func (callable): Функция-предикат (возвращает True/False).
        array (list): Список для фильтрации.

    Returns:
        list: Отфильтрованный список.
    """
    return [item for item in array if func(item)]

# Данные
data = ["apple", "banana", "kiwi", "grape", "orange juice", "avocado", "cat"]

# 1. Исключить строки с пробелами
no_spaces = lambda s: ' ' not in s
result1 = filter_array(no_spaces, data)
print(f"1. Без пробелов: {result1}")

# 2. Исключить строки, начинающиеся с буквы 'а'
not_starts_with_a = lambda s: not s.startswith('a')
result2 = filter_array(not_starts_with_a, data)
print(f"2. Не начинаются на 'a': {result2}")

# 3. Исключить строки, длина которых меньше 5
length_at_least_5 = lambda s: len(s) >= 5
result3 = filter_array(length_at_least_5, data)
print(f"3. Длина >= 5: {result3}")