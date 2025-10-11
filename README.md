# FlaskAPI-Core

Flask authentication boilerplate with JWT, SQLAlchemy and Flask-Smorest.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
    - [Local setup](#local-setup)
    - [Docker setup](#docker-setup)
- [Database Schema](#database-schema)
- [Endpoints](#endpoints)
    - [Auth](#auth)
    - [Test auth](#test-auth)
    - [User management (dev only)](#user-management-dev-only)
- [Validation and Errors](#validation-and-errors)
- [Testing](#testing)

---

## Features

- User registration and login with hashed passwords (`passlib`)
- JWT authentication (access + refresh tokens)
- Token revocation using blocklist
- Protected and fresh-protected endpoints
- API documentation with **Swagger UI** (via Flask-Smorest) available at [`/swagger-ui`](http://localhost:5000/swagger-ui)
- Database migrations with **Flask-Migrate / Alembic**
- Environment variable support via `.env` / `.flaskenv`
- Docker and docker-compose setup
- Unit and integration tests with **pytest**

---

## Requirements

- Python 3.13
- Flask
- Flask-Smorest
- SQLAlchemy
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Passlib
- python-dotenv
- Docker (optional, for containerized dev/prod)

See [requirements.txt](requirements.txt) and [requirements-dev.txt](requirements-dev.txt).

---

## Installation

### Local setup

- Clone repository

```bash
git clone https://github.com/mateusz-przybyla/FlaskAuthTemplate.git
cd FlaskAuthTemplate
```

- Create virtual environment (Windows Powershell)

```bash
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install dependencies

```bash
pip install -r requirements-dev.txt
```

- Copy environment variables file

```bash
copy .env.example .env (Windows Powershell)
# then edit .env and set your values, e.g.:
# FLASK_CONFIG=development
# JWT_SECRET_KEY=super-secret-key
# DATABASE_URL=sqlite:///data-dev.db
```

- Initialize database

```bash
flask db upgrade
```

- Run app

```bash
flask run
```

### Docker setup

- Copy environment variables file

```bash
copy .env.example .env (Windows Powershell)
# then edit .env and set your values, e.g.:
# FLASK_CONFIG=development
# JWT_SECRET_KEY=super-secret-key
# DATABASE_URL=sqlite:///data-dev.db
```

- Build image and start container

```bash
docker-compose up -d --build
```

- Run migrations inside container

```bash
docker-compose exec web flask db upgrade
```

- Check logs

```bash
docker-compose logs -f
```

- Stop docker container

```bash
docker-compose down
```

---

## Database Schema

![](/readme/database-schema.jpg)

---

## Endpoints

### Auth

- **POST** `/register`\
  Register a new user.\
  **Request:** `{ "email": "user@example.com", "password": "secret123" }`\
  **Response:** `{ "message": "User created successfully." }`, `201 Created`\
  **Errors:**
    - `409 Conflict` → email already exists
    - `500 Internal Server Error` → database issue

- **POST** `/login`\
  Authenticate user and return tokens.\
  **Request:** `{ "email": "user@example.com", "password": "secret123" }`\
  **Response:** `{ "access_token": "...", "refresh_token": "..." }`, `200 OK`\
  **Errors:**
    - `401 Unauthorized` → invalid credentials

- **POST** `/refresh`\
  Get new access token using refresh token.\
  **Headers:** `Authorization: Bearer <refresh_token>`\
  **Response:** `{ "access_token": new_token}`, `200 OK`\
  **Errors:**
    - `401 Unauthorized` → expired/invalid/blacklisted refresh token

- **POST** `/logout`\
  Revoke current access token.\
  **Headers:** `Authorization: Bearer <access_token>`\
  **Response:** `{ "message": "Successfully logged out." }`, `200 OK`

### Test Auth

Endpoints for verifying JWT behavior:

- **GET** `/guest` → open for everyone (no token required)
- **GET** `/protected` → requires valid access token
- **GET** `/fresh-protected` → requires fresh token (i.e. directly from login, not from refresh)

### User management (dev only)

- **GET** `/user/<id>`\
  Fetch user by id.\
  **Response:** `200 OK` → with user data\
  **Errors:** 
    - `404 Not Found` → if user doesnt't exist
- **DELETE** `/user/<id>`\
  Delete user.\
  **Response:** `{ "message": "User deleted." }`, `200 OK`\
  **Errors:**
    - `404 Not Found` → if user doesnt't exist
    - `500 Internal Server Error` → on database issue

---

## Validation and Errors

- Common JWT errors (always return `401 Unauthorized`)
    - Missing token

    ```json
    {
        "message": "Request does not contain an access token.",
        "error": "authorization_required"
    }
    ```

    - Invalid token

    ```json
    {
        "message": "Signature verification failed.",
        "error": "invalid_token"
    }
    ```

    - Expired token

    ```json
    {
        "message": "The token has expired.",
        "error": "token_expired"
    }
    ```    

    - Revoked token

    ```json
    {
        "message": "The token has been revoked.",
        "error": "token_revoked"
    }
    ```  

    - Non-fresh token on fresh-only endpoint

    ```json
    {
        "message": "The token is not fresh.",
        "error": "fresh_token_required"
    }
    ```      

- Validation errors (`422 Unprocessable Entity`)

  If request body fails schema validation (Marshmallow), errors are returned per field:

    ```json
    {
        "email": ["Not a valid email address."],
        "password": ["Shorter than minimum length 6."]
    }
    ```

- Resource errors
    - Duplicate user (`409 Conflict`)

    ```json
    {
        "message": "A user with that email already exists."
    }
    ```

    - User not found (`404 Not Found`)

    ```json
    {
        "message": "User not found."
    }
    ```

    - Database errors (`500 Internal Server Error`)

    ```json
    {
        "message": "An error occurred while creating the user."
    }
    ```

---

## Testing

Run all tests:

```bash
pytest -v
```

Run all tests with coverage:

```bash
pytest -v --cov=app tests/
```

Run all tests with coverage via Docker:

```bash
docker-compose exec web pytest -v --cov=app tests/
```

Test structure:
- `tests/unit/` → models, schemas
- `tests/integration/` → auth flow, protected endpoints