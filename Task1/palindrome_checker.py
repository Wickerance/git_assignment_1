# Palindrome Checker
def is_palindrome(text):
    cleaned_text = ''.join(filter(str.isalnum, text)).lower()
    return cleaned_text == cleaned_text[::-1]
print(f"'madam': {is_palindrome('madam')}")        
print(f"'A man, a plan, a canal: Panama': {is_palindrome('A man, a plan, a canal: Panama')}") 
print(f"'hello': {is_palindrome('hello')}")      