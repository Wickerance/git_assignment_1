## Project Context: Assignment 4 - FastAPI Authentication Service

This project is a Python application built using the FastAPI framework, primarily focused on user authentication via JSON Web Tokens (JWT) and token refresh mechanisms.

### Core Stack & Technologies:

* **Backend:** Python 3.11, FastAPI
* **Data Models:** Pydantic (for request/response validation and serialization)
* **Authentication:** JWT (Access and Refresh Tokens), Password Hashing (passlib)
* **Dependencies:** Docker, PostgreSQL (Database), Redis (Cache/Session - where token blacklisting will occur)

### Key Files and Directories:

1.  **`app/main.py`**:
    * **Purpose:** Contains the main FastAPI application instance and defines all API endpoints (e.g., `/register`, `/login`, `/refresh`, `/me`).
    * **Dependencies:** Imports models and functions from `app/schemas.py` and `app/security.py`.

2.  **`app/schemas.py`**:
    * **Purpose:** Defines all Pydantic models, including `UserAuth`, `UserBase`, `UserDisplay`, `Token`, and `TokenRefresh`.

3.  **`app/security.py`**:
    * **Purpose:** Contains core security logic (password verification, token generation, token validation, and the `get_current_user` dependency).

4.  **`app/service.py`**:
    * **Purpose:** Contains business logic for user creation, authentication, and token refreshing, interfacing between the routes and the database.

### Primary Guidance for AI Assistants:

* **Token Types:** The application uses two types of tokens: `access` (short-lived, for resource access) and `refresh` (long-lived, for token renewal).
* **Token Refresh Logic:** The `/refresh` endpoint must use the long-lived refresh token to issue a new pair of access and refresh tokens.
* **Database/Auth Separation:** All security and token logic is contained in `app/security.py`, while user and login history persistence is handled by the services layer (`app/service.py`).
* **Pydantic Use:** When generating code related to request/response bodies, always reference the Pydantic models defined in `app/schemas.py`.
```eof

