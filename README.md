# 🚀 Simple Flask Authentication Service

Welcome to your new go-to Flask-based authentication service! This streamlined solution offers a robust foundation for mastering authentication essentials. With built-in features like user login, registration, token management, and MongoDB integration, it’s designed to be user-friendly and versatile.

### 🌟 Key Features

- **🔐 User Login:** Securely authenticate users with password verification.
- **📝 User Registration:** Effortlessly create new user accounts.
- **🎫 Token Generation:** Issue secure tokens upon successful login for access control.
- **⏳ Token Expiration:** Manage token validity to enhance security.
- **🌍 Language Agnostic:** Seamlessly integrates with projects in any programming language.
- **💾 MongoDB Integration:** Uses MongoDB and an Object-Document Mapper (ODM) for reliable data persistence.

### 🚀 Getting Started

#### 📋 Prerequisites

Ensure you have the following:

- Python 3.6 or later ([Download Python](https://www.python.org/))
- Flask web framework ([Check Flask](https://flask.palletsprojects.com/))
- MongoDB database ([Explore MongoDB](https://www.mongodb.com/))

#### 🏃‍♂️ Running the Service

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/flask-authentication-service.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd flask-authentication-service
    ```
3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Server:**

    ```bash
    python server.py
    ```

5. **Access the Service:**
   Your authentication service will be available at `localhost:9999` (port is customizable).

### 📡 API Endpoints

| **Method** | **Path**                    | **Description** |
|------------|-----------------------------|-----------------|
| `POST`      | `/login`                    | Login a user and obtain a token (provide `id` and `password` in the request body). |
| `POST`      | `/register`                 | Register a new user (provide `id` and `password` in the request body). |
| `POST`      | `/getUserIdWithToken`       | Retrieve the user ID associated with a specific token (provide `token` in the request body). |
| `POST`      | `/isTokenExpired`           | Check if a token has expired (provide `token` in the request body). |

### 💡 Example Usage (with cURL)

**Login:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": "your_user_id", "password": "your_password"}' http://localhost:9999/login
```

**Register:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"id": "new_user_id", "password": "new_user_password"}' http://localhost:9999/register
```

Feel free to explore, customize, and make this service your own. Happy coding! 😄
