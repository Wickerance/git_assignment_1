## Project Context: Assignment 2 - Python Fundamentals (Functions, Classes, Decorators)

This project focuses on fundamental Python programming concepts, including functions, higher-order functions (lambda), object-oriented programming (inheritance, methods), and decorators. The project structure is task-based, with separate folders or files dedicated to each problem.

### Core Stack & Technologies:

* **Backend:** Python 3.11+
* **Libraries:** Standard Python library only.
* **Execution:** Designed for script execution (e.g., `python task_name.py`) or module testing.

### Key Tasks and Logic:

1.  **Palindrome Check:** Write a function that checks if a string is a palindrome.
2.  **Higher-Order Filtering:** Write a function that accepts a lambda filter function and a list of strings. Test it with filters to:
    * Exclude strings with spaces.
    * Exclude strings starting with the letter 'a'.
    * Exclude strings shorter than 5 characters.
3.  **Shape Hierarchy:** Create a class hierarchy for Shapes: Square, Rectangle, Triangle, Circle. Each class must implement methods for:
    * Calculating area.
    * Calculating perimeter.
    * Comparing area with another figure (greater or less).
    * Comparing perimeter with another figure (greater or less).
4.  **Student Hierarchy:** Create `Student` and `GraduateStudent` classes. `Student` includes properties: group number, average grade (GPA). `GraduateStudent` is differentiated by having a scientific work title (string). Implement methods to:
    * Display personal information (full name, age).
    * Calculate scholarship amount (5.0 GPA: Graduate 8000₽, Student 6000₽; < 5.0 GPA: Graduate 6000₽, Student 4000₽; else 0₽).
    * Compare scholarship amount with another student/graduate.
5.  **Timing Decorator:** Implement a decorator that prints the execution time of the decorated function. Test it on:
    * A function that calculates and prints the sum of two numbers (a + b).
    * A function that reads two numbers (a, b) from `input.txt` and writes the result to `output.txt`.

### Primary Guidance for AI Assistants:

* **OOP Focus (Tasks 3 & 4):** Ensure correct use of inheritance and comparison methods (`__lt__`, `__gt__`) where appropriate.
* **Modularity:** Separate each task into distinct functions or modules for clarity.
* **Error Handling:** Implement robust error handling, especially for file operations (Task 5).
```eof

