# 🏥 Patient Visit History API

A RESTful Patient Visit History Management API built using **FastAPI** following a **Layered Architecture** (Router → Service → Repository). The application allows authenticated administrators to search patient visit history, create appointments, and update appointment details using JWT-based authentication.

---

## 🚀 Features

- 🔐 JWT Authentication
- 👨‍⚕️ Admin Login
- 🔎 Dynamic Patient Visit History Search
- ➕ Create New Appointments
- ✏️ Update Existing Appointments
- ✅ Request Validation using Pydantic
- ⚠️ Custom Exception Handling
- 📝 Centralized Logging
- 📂 SQL Queries Stored in YAML Files
- 💉 SQLite Database
- 🔄 Dependency Injection
- 🏗️ Repository-Service Pattern

---

## 📁 Project Structure

```
.
├── app
│   ├── auth
│   ├── database
│   ├── queries
│   ├── repositories
│   ├── routers
│   ├── schemas
│   ├── services
│   ├── utils
│   ├── dependencies.py
│   └── main.py
├── logs
├── 01_schema.sql
├── 02_seed_data.sql
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- Python 3.12
- FastAPI
- SQLite
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- PyYAML
- Uvicorn

---

## 🏛️ Architecture

```
                Client
                   │
                   ▼
              FastAPI Router
                   │
                   ▼
                Service Layer
                   │
                   ▼
             Repository Layer
                   │
                   ▼
             SQLite Database
```

---

## 🔐 Authentication

The application uses **JWT Bearer Authentication**.

### Login

```
POST /auth/login
```

Example Request

```json
{
    "username": "admin",
    "password": "admin123"
}
```

Example Response

```json
{
    "access_token": "<JWT_TOKEN>",
    "token_type": "Bearer"
}
```

Use the generated JWT token in Swagger's **Authorize** button.

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/login` | Admin Login |

---

### Appointments

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/appointments/history` | Search Patient Visit History |
| POST | `/appointments/appointments` | Create Appointment |
| PUT | `/appointments/appointments/{appointment_id}` | Update Appointment |

---

## 🔎 Search Filters

Patient visit history supports filtering by:

- Patient ID
- Doctor ID
- Department
- Appointment Status
- Start Date
- End Date

Filters can be combined to perform dynamic searches.

---

## ⚠️ Exception Handling

Custom exceptions implemented:

- Patient Not Found
- Doctor Not Found
- Appointment Not Found
- Invalid Credentials
- Invalid Appointment Status
- Invalid Date Range
- Diagnosis Required
- Unauthorized Access

All exceptions return structured JSON responses.

---

## 📝 Logging

The application maintains centralized logs for:

- Login Requests
- Search Requests
- Appointment Creation
- Appointment Updates
- Database Errors
- Exceptions

Logs are stored inside:

```
logs/application.log
```

---

## 📂 SQL Query Management

Instead of hardcoding SQL queries throughout the codebase, all SQL statements are stored in YAML files.

```
queries/
    appointment.yaml
    auth.yaml
```

Queries are loaded dynamically using a custom query loader.

---

## ▶️ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/patient-visit-history-api.git
```

Move into the project

```bash
cd patient-visit-history-api
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## ✅ Key Concepts Implemented

- FastAPI
- REST API Development
- Layered Architecture
- Repository Pattern
- Dependency Injection
- JWT Authentication
- Role-Based Authorization
- Password Hashing (bcrypt)
- Pydantic Validation
- SQL Query Management using YAML
- Logging
- Exception Handling

---

## 📜 License

This project is developed for educational purposes.
