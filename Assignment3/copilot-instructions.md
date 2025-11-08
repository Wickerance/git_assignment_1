## Project Context: Assignment 3 - FastAPI CRUD Service (Students and Groups)

This project is a RESTful API service using the FastAPI framework to manage data about students and groups (Student Group API Project). It implements full Create, Read, Update, and Delete (CRUD) operations and specific business logic for managing the relationship between students and groups.

### Core Stack & Technologies:

* **Backend:** Python 3.11, FastAPI
* **Data Models:** Pydantic (for API request/response modeling and validation)
* **Database:** PostgreSQL (Docker-based)
* **ORM:** SQLAlchemy (Async mode preferred)

### Key Files and Directories:

1. **`app/main.py`**:
   * **Purpose:** Defines the main application instance and all API routes (e.g., POST `/students`, PUT `/students/{id}/group/{group_id}`, DELETE `/groups/{id}`).
   * **Focus:** Dependency Injection (DB Session), calling the service/CRUD layer functions.

2. **`app/models.py`**:
   * **Purpose:** Defines SQLAlchemy ORM declarative models (`Student`, `Group`). This represents the **database schema** definition.
   * **Relationships:** Note the foreign key relationship where `Student.group_id` links to `Group.id`.

3. **`app/schemas.py`**:
   * **Purpose:** Defines Pydantic models (e.g., `StudentCreate`, `StudentUpdate`, `GroupDisplay`). This is the **API data contract**.
   * **Important:** All API request bodies and response structures must use models defined here.

4. **`app/service.py` / `app/crud.py`**:
   * **Purpose:** Contains all database interaction logic and business rules.

### Primary Guidance for AI Assistants:

* **Business Logic:** The logic for deleting a group (`DELETE /groups/{id}`) must be handled carefully. It should not delete the associated students; instead, it must ensure the deleted group's ID is set to `NULL` for any students previously belonging to that group.
* **Layer Separation:** Database interaction should strictly use SQLAlchemy ORM models from `app/models.py` and be confined to the service/CRUD layer.
* **Data Transfer:** Use Pydantic schemas from `app/schemas.py` exclusively for API request and response data handling.
```eof

