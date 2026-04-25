# 🚀 E-commerce platform - Backend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

This is a high-performance RESTful API design for an e-commerce platform. Developed using Flask, the architecture implements a modular system based on Blueprints that separates the domains of administration and client. The projects stand out for the use of the repository pattern, which ensures total decoupling between business logic and data persistence with SQLAlchemy. Additionally, a strict serialization by Marshmallow is implemented to guarantee the integrity of JSON responses.

## Technologies

- **Flask**: For a lightweight and modular RESTful architecture
- **SQLAlchemy & PostgreSQL**: Robust data persistence and relational mapping
- **Marshmallow**: Strict data validation and serialization
- **JWT**: Secure stateless authentication

## 🛠️ Installation and Configuration

Follow these steps to raise the development environment locally

### 1. Clone this repository

```Bash
git clone https://github.com/sebastiansaenz-dev/DUAD.git
cd DUAD/backend_project
```

### 2. Create and Activate the Virtual Environment

```Bash
# Create the virtual environment
python -m venv .venv

# Activate the environment
# On Mac/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```Bash
pip install -r requirements.txt
```

### 4. Environment Configuration

- Create your .env file and fill your local credentials

```Bash
cp .env.example .env
```

- Create your .env file and fill your local credentials

```
DATABASE_URL=your_data_base_url
SECRET_KEY=your_secret_key
```

### 5. Database initialization

```Bash
# Apply the migrations to create your database tables
flask db upgrade
```

### 6. Run the Application

```Bash
python app.py
```

### 🚀 The API will be running at: http://localhost:5002

## 🔌 API Routes Flow

### 🔒 Authentication

- **Login** ➤ `POST` ➔ `/users/login` ➔ Returns JWT Token and user profile

- **Register** ➤ `POST` ➔ `/users/register-user` ➔ Returns new user profile and JWT Token

### 👤 Client Endpoints

- **Products** ➤ `GET` `/products` ➜ List All Items

- **Add products to cart** ➤ `POST` `/carts` ➜ Add products to cart

### 🛠️ Admin Endpoints

- **Add Product** ➤ `POST` `/staff-portal/products` ➜ [Auth Required]

- **Update** ➤ `PATCH` `/staff-portal/products/<id>` ➜ [Auth Required]

- **Delete** ➤ `DELETE` `/staff-portal/products/<id>` ➜ [Auth Required]

## 🔐 Login Example

### Example Request Body:

```JSON
{
    "email": "dev@example.com",
    "password": "your_secure_password"
}
```

### Example Successful Response:

```JSON
{
    "message": "login successfully",
    "token": "eyJhbGciOiJSUzI1NiIsIn...",
    "user": {
        "email": "dev@example.com",
        "id": 4,
        "roles": [
            {
                "id": 2,
                "name": "client"
            }
        ],
        "username": "DevExample"
    }
}
```
