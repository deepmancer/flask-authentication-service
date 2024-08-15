# A Simple Flask Authentication Service 

This is a basic authentication service built with Flask to provide a foundation for understanding authentication concepts. It offers core functionalities for user login, registration, and token management.

**Key Features:**

* ** User Login:** Authenticate users with secure password verification.
* **‍daftar User Registration:** Create new user accounts with ease.
* ** Token Generation:** Issue tokens upon successful login for secure access control.
* **⏳ Token Expiration:** Enforce token validity periods to enhance security.
* ** Language Agnostic:** Works seamlessly with projects in any programming language.

**Getting Started**

**Prerequisites:**

- Python 3.6 or later ([ Python](https://www.python.org/))
- Flask web framework ([ Flask](https://flask.palletsprojects.com/))
- MongoDB database ([ MongoDB](https://www.mongodb.com/))

**Running the Service:**
1. Clone Clone this repository:

```bash
git clone https://github.com/your-username/flask-authentication-service.git
```

2. Navigate to the project directory:

```bash
cd flask-authentication-service
```

3. Start the server:

```bash
python server.py
```

4. Your authentication service will be running on `localhost:9999` (port can be customized).

**API Endpoints:**

| **Method** | **Path** | **Description** |
|---|---|---|
| POST | `/login` | Login a user and obtain a token (provide `id` and `password` in request body). |
| POST | `/register` | Register a new user (provide `id` and `password` in request body). |
| POST | `/getUserIdWithToken` | Get the user ID associated with a specific token (provide `token` in request body). |
| POST | `/isTokenExpired` | Check if a token has expired (provide `token` in request body). |

**Example Usage (using cURL):**

**Login:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": "your_user_id", "password": "your_password"}' http://localhost:9999/login
```

**Register:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": "new_user_id", "password": "new_user_password"}' http://localhost:9999/register
```
