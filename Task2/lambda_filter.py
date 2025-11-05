# Lambda Filter
def filter_arr(func, arr):
    return [s for s in arr if func(s)]

# Данные
data = ["apple", "banana", "kiwi", "grape", "orange juice", "avocado", "cat"]

# 1. Исключить строки с пробелами
no_spaces = lambda s: ' ' not in s
result1 = filter_arr(no_spaces, data)
print(f"1. Без пробелов: {result1}")

# 2. Исключить строки, начинающиеся с буквы 'а'
not_starts_with_a = lambda s: not s.startswith('a')
result2 = filter_arr(not_starts_with_a, data)
print(f"2. Не начинаются на 'a': {result2}")

# 3. Исключить строки, длина которых меньше 5
length_at_least_5 = lambda s: len(s) >= 5
result3 = filter_arr(length_at_least_5, data)
print(f"3. Длина >= 5: {result3}")