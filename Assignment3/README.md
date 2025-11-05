Student Group API Project (Задание 3)

Данный проект реализует RESTful API для управления информацией о студентах и группах на базе FastAPI и PostgreSQL. Выполнены все функциональные и инфраструктурные требования задания.

Развертывание и Запуск

Требования к окружению
- Docker
- Docker Compose

Процесс запуска

1.  Клонирование проекта:
    git clone https://github.com/Wickerance/git_assignment_1/
    
2.  Переход в папку проекта:
    cd git_assignment_1/Assignment3/
    
3.  Настройка переменных окружения:
    Используйте .env.example как шаблон конфигурации.
    cp .env.example .env
    # Отредактируйте файл .env и введите учетные данные базы данных

4.  Сборка и запуск сервисов:
    docker compose up --build -d

5.  Доступ к API:
    Документация API (Swagger UI): http://localhost:8000/docs

Контрольный список функций

Все функции успешно протестированы и соответствуют требованиям задания:

Функция | Метод HTTP | Маршрут | Результат
CRUD Студенты | POST, GET, DELETE | /students/ & /groups/ | PASS
CRUD Группы | POST, GET, DELETE | /students/ & /groups/ | PASS
Перевод студента в группу (A -> B) | PUT | /students/{id}/group/{group_id} | PASS
Бизнес-логика удаления группы | DELETE | /groups/{id} | PASS (Проверено: group_id студента устанавливается в NULL)
Получение списка студентов в группе | GET | /groups/{id}/students | PASS

Состояние инфраструктуры

- [x] Код разделен на слои (API, Service, DB Model).
- [x] Конфигурация базы данных определена в docker-compose.yml.
- [x] Предоставлен шаблон переменных окружения (.env.example).
- [x] Предоставлен файл requirements.txt.