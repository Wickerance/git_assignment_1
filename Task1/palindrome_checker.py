"""
Модуль для проверки строк на палиндром.
"""

def is_palindrome(text):
    """
    Проверяет, является ли текст палиндромом.
    
    Игнорирует регистр и небуквенные символы.

    Args:
        text (str): Строка для проверки.

    Returns:
        bool: True, если текст является палиндромом, иначе False.
    """
    cleaned_text = ''.join(filter(str.isalnum, text)).lower()
    return cleaned_text == cleaned_text[::-1]

if __name__ == "__main__":
    print(f"'madam': {is_palindrome('madam')}")        
    print(f"'A man, a plan, a canal: Panama': {is_palindrome('A man, a plan, a canal: Panama')}") 
    print(f"'hello': {is_palindrome('hello')}")