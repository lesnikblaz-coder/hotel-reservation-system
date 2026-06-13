# Hotel Reservation System

A hotel reservation management API built with FastAPI, PostgreSQL, and SQLAlchemy ORM, following a layered architecture with separate API, service, and data access layers.

This project started as a command-line application using SQLite and was later refactored into a secure REST API using FastAPI, PostgreSQL, JWT authentication, and role-based access control as part of my backend development learning journey.

## Features

### Authentication & Authorization

* User registration
* User login
* JWT access token generation
* OAuth2 password flow support
* Protected API endpoints
* Role-based access control (RBAC)
* Authorization policies for Guests, Staff, and Administrators
* Password hashing and verification

### User Management

* View all users (Admin)
* Retrieve user details (Admin)
* Update user information (Admin)
* Delete users (Admin)

### Guest Management

* Create guests
* View all guests
* Retrieve guest details
* Update guest information
* Delete guests

### Room Management

* Create rooms
* View all rooms
* Retrieve room details
* Update room information
* Delete rooms
* Activate/deactivate rooms
* Search room availability for a date range

### Reservation Management

* Create reservations
* View all reservations
* Retrieve reservation details
* Update reservations
* Cancel reservations
* Check guests in
* Check guests out
* Prevent overlapping reservations for the same room

### Reporting & Analytics

* Revenue reports for custom date ranges
* Monthly revenue reports
* Yearly revenue reports
* Current occupancy reports
* Monthly occupancy reports

### Testing

* Comprehensive FastAPI endpoint test suite
* Positive and negative test cases
* Request validation testing
* Authentication and authorization testing
* Error handling verification
* Isolated test database setup using pytest fixtures

## Role-Based Access Control

The API uses three authorization levels:

| Role  | Permissions                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| Guest | Register, login, create reservations, search room availability, manage guest records                                  |
| Staff | All Guest permissions plus view guests, rooms, reservations, occupancy reports, perform check-in/check-out operations |
| Admin | Full system access including room management, reservation updates, revenue reports, and user management               |

## API Endpoints

### Authentication

| Method | Endpoint         | Description                      |
| ------ | ---------------- | -------------------------------- |
| POST   | `/auth/register` | Register a new user              |
| POST   | `/auth/login`    | Login and receive JWT token      |
| POST   | `/auth/token`    | OAuth2-compatible token endpoint |

### Users (Admin Only)

| Method | Endpoint           | Description      |
| ------ | ------------------ | ---------------- |
| GET    | `/users`           | Get all users    |
| GET    | `/users/{user_id}` | Get user details |
| PUT    | `/users/{user_id}` | Update user      |
| DELETE | `/users/{user_id}` | Delete user      |

### Guests

| Method | Endpoint             | Access             |
| ------ | -------------------- | ------------------ |
| POST   | `/guests`            | Authenticated User |
| GET    | `/guests`            | Staff+             |
| GET    | `/guests/{guest_id}` | Staff+             |
| PUT    | `/guests/{guest_id}` | Admin              |
| DELETE | `/guests/{guest_id}` | Admin              |

### Rooms

| Method | Endpoint                      | Access             |
| ------ | ----------------------------- | ------------------ |
| POST   | `/rooms`                      | Admin              |
| GET    | `/rooms`                      | Staff+             |
| POST   | `/rooms/availability`         | Authenticated User |
| GET    | `/rooms/{room_id}`            | Staff+             |
| PUT    | `/rooms/{room_id}`            | Admin              |
| DELETE | `/rooms/{room_id}`            | Admin              |
| POST   | `/rooms/{room_id}/activate`   | Admin              |
| POST   | `/rooms/{room_id}/deactivate` | Admin              |

### Reservations

| Method | Endpoint                                   | Access             |
| ------ | ------------------------------------------ | ------------------ |
| POST   | `/reservations`                            | Authenticated User |
| GET    | `/reservations`                            | Staff+             |
| GET    | `/reservations/{reservation_id}`           | Staff+             |
| PUT    | `/reservations/{reservation_id}`           | Admin              |
| POST   | `/reservations/{reservation_id}/cancel`    | Staff+             |
| POST   | `/reservations/{reservation_id}/check-in`  | Staff+             |
| POST   | `/reservations/{reservation_id}/check-out` | Staff+             |

### Reports

| Method | Endpoint                     | Access |
| ------ | ---------------------------- | ------ |
| POST   | `/reports/revenue`           | Admin  |
| GET    | `/reports/revenue/monthly`   | Admin  |
| GET    | `/reports/revenue/yearly`    | Admin  |
| GET    | `/reports/occupancy/today`   | Staff+ |
| POST   | `/reports/occupancy/monthly` | Staff+ |

## Security

The API is secured using JWT bearer tokens.

### Authentication Flow

1. Register a user via `/auth/register`
2. Login via `/auth/login` or `/auth/token`
3. Receive a JWT access token
4. Include the token in requests:

```http
Authorization: Bearer <access_token>
```

### Authorization

Protected endpoints enforce role-based access control using FastAPI dependency injection.

### Role Permissions Matrix

| Action                    | Guest | Staff | Admin |
| ------------------------- | :---: | :---: | :---: |
| Register account          |   ✅   |   ✅   |   ✅   |
| Login                     |   ✅   |   ✅   |   ✅   |
| Create guest record       |   ✅   |   ✅   |   ✅   |
| View guests               |   ❌   |   ✅   |   ✅   |
| View guest details        |   ❌   |   ✅   |   ✅   |
| Update guests             |   ❌   |   ❌   |   ✅   |
| Delete guests             |   ❌   |   ❌   |   ✅   |
| Search room availability  |   ✅   |   ✅   |   ✅   |
| Create reservation        |   ✅   |   ✅   |   ✅   |
| View reservations         |   ❌   |   ✅   |   ✅   |
| View reservation details  |   ❌   |   ✅   |   ✅   |
| Cancel reservation        |   ❌   |   ✅   |   ✅   |
| Check in guests           |   ❌   |   ✅   |   ✅   |
| Check out guests          |   ❌   |   ✅   |   ✅   |
| View rooms                |   ❌   |   ✅   |   ✅   |
| Create rooms              |   ❌   |   ❌   |   ✅   |
| Update rooms              |   ❌   |   ❌   |   ✅   |
| Delete rooms              |   ❌   |   ❌   |   ✅   |
| Activate/deactivate rooms |   ❌   |   ❌   |   ✅   |
| View occupancy reports    |   ❌   |   ✅   |   ✅   |
| View revenue reports      |   ❌   |   ❌   |   ✅   |
| View users                |   ❌   |   ❌   |   ✅   |
| Update users              |   ❌   |   ❌   |   ✅   |
| Delete users              |   ❌   |   ❌   |   ✅   |

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic
* Pydantic
* JWT Authentication
* OAuth2 Password Flow
* Password Hashing
* Pytest

## Project Evolution

This project went through several iterations:

1. Started as a command-line hotel reservation application.
2. Used SQLite as the initial database.
3. Refactored into a layered architecture.
4. Migrated database storage from SQLite to PostgreSQL.
5. Converted the application into a FastAPI REST API.
6. Introduced SQLAlchemy ORM for database modeling and data access.
7. Added Alembic database migrations for schema versioning.
8. Implemented reporting and analytics endpoints.
9. Added JWT authentication and authorization.
10. Implemented role-based access control (Guest, Staff, Admin).
11. Added user management functionality.
12. Added comprehensive automated API testing with Pytest.

## Architecture

The application is organized into separate layers to improve maintainability and separation of concerns:

### API Layer

* Defines FastAPI routes and handles HTTP requests and responses.

### Service Layer

* Contains business logic for authentication, users, guests, rooms, reservations, and reporting.
* Enforces business rules and authorization requirements.

### Data Access Layer

* Handles database operations through repository abstractions.

### Database Layer

* SQLAlchemy ORM models.
* PostgreSQL database integration.
* Alembic migration support.

### Validation Layer

* Pydantic schemas for request validation and response serialization.

### Security Layer

* JWT token creation and validation.
* Password hashing and verification.
* OAuth2 integration.
* Role-based authorization dependencies.

### Error Handling

* Custom application exceptions.
* Centralized exception handlers for consistent API responses.

## Installation

Clone the repository:

```bash
git clone https://github.com/lesnikblaz-coder/hotel-reservation-system.git
cd hotel-reservation-system
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/hotel_db
```

## Database Migrations

This project uses Alembic for database schema migrations.

Apply all pending migrations:

```bash
alembic upgrade head
```

Create a new migration after modifying SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe changes"
```

View migration history:

```bash
alembic history
```

## Running the Application

```bash
uvicorn api:app --reload
```

## API Documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
python -m pytest -v
```

## Key Learning Outcomes

* REST API design with FastAPI
* JWT authentication and authorization
* Role-based access control (RBAC)
* OAuth2 password flow
* Password hashing and security best practices
* SQLAlchemy ORM relationships and querying
* Database schema design
* Layered application architecture
* Input validation with Pydantic
* Automated testing with Pytest

## Future Improvements

* Refresh tokens
* Password reset flow
* Docker + Docker Compose
* GitHub Actions (CI/CD)
* Deploy to Render
* API rate limiting
* Audit logging
* Caching with Redis