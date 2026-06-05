# Hotel Reservation System

A hotel reservation management API built with FastAPI, PostgreSQL, and SQLAlchemy ORM, following a layered architecture with separate API, service, and data access layers.

This project started as a command-line application using SQLite and was later refactored into a REST API using FastAPI and PostgreSQL as part of my backend development learning journey.

### Features

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
* Check room availability

### Reservation Management

* Create reservations
* View all reservations
* Retrieve reservation details
* Cancel reservations
* Check guests in
* Check guests out
* Prevents overlapping reservations for the same room

## API Endpoints

## API Endpoints

### Guests

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| GET    | `/guests`            | Get all guests    |
| POST   | `/guests`            | Create a guest    |
| GET    | `/guests/{guest_id}` | Get a guest by ID |
| PUT    | `/guests/{guest_id}` | Update a guest    |
| DELETE | `/guests/{guest_id}` | Delete a guest    |

### Rooms

| Method | Endpoint                      | Description                             |
| ------ | ----------------------------- | --------------------------------------- |
| GET    | `/rooms`                      | Get all rooms                           |
| POST   | `/rooms`                      | Create a room                           |
| POST   | `/rooms/availability`         | Search available rooms for a date range |
| GET    | `/rooms/{room_id}`            | Get a room by ID                        |
| PUT    | `/rooms/{room_id}`            | Update a room                           |
| DELETE | `/rooms/{room_id}`            | Delete a room                           |
| POST   | `/rooms/{room_id}/activate`   | Activate a room                         |
| POST   | `/rooms/{room_id}/deactivate` | Deactivate a room                       |

### Reservations

| Method | Endpoint                                   | Description                 |
| ------ | ------------------------------------------ | --------------------------- |
| GET    | `/reservations`                            | Get all reservations        |
| POST   | `/reservations`                            | Create a reservation        |
| GET    | `/reservations/{reservation_id}`           | Get reservation details     |
| PUT    | `/reservations/{reservation_id}`           | Update a reservation        |
| POST   | `/reservations/{reservation_id}/cancel`    | Cancel a reservation        |
| POST   | `/reservations/{reservation_id}/check-in`  | Check in a guest            |
| POST   | `/reservations/{reservation_id}/check-out` | Check out a guest           |
| GET    | `/reservations/{reservation_id}/price`     | Calculate reservation price |


## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic
* Pydantic
* Pytest

## Project Evolution

This project went through several iterations:

1. Started as a command-line hotel reservation application.
2. Used SQLite as the initial database.
3. Refactored into a layered architecture.
4. Migrated database storage from SQLite to PostgreSQL.
5. Converted the application into a FastAPI REST API.
6. Introduced SQLAlchemy ORM for database modeling and data access.
7. Added Alembic database migrations for schema versioning and database change management.

## Architecture

The application is organized into separate layers to improve maintainability and separation of concerns:

### API Layer

* `api.py` defines the FastAPI routes and handles HTTP requests and responses.

### Service Layer

* `services/` contains the business logic for guest, room, and reservation operations.
* Business rules such as room availability checks and reservation validation are handled here.

### Data Access Layer

* `repository.py` is responsible for database operations and acts as the interface between the application and the database.

### Database Layer

* `database.py` manages database connections and SQLAlchemy session configuration.
* `models.py` defines the SQLAlchemy ORM models that map Python classes to PostgreSQL tables.

### Validation Layer

* `schemas.py` contains Pydantic models used for request validation and API response serialization.

### Error Handling

* `exceptions.py` defines custom application exceptions.
* `exception_handlers.py` converts application exceptions into appropriate HTTP responses.


## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/hotel-reservation-system.git
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

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
pytest
```

## Key Learning Outcomes

- REST API design with FastAPI
- Database schema design
- SQLAlchemy ORM relationships and querying
- Business rule enforcement (preventing overlapping reservations)
- Layered application architecture
- Input validation with Pydantic
- Automated testing with Pytest

## Future Improvements

- Expand FastAPI test coverage
- JWT Authentication
- Authorization
- Role-based access control
- Docker + Docker Compose
- GitHub Actions (CI)
- Deploy to Render
- API rate limiting