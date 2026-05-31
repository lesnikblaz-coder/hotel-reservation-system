# Hotel Reservation System

A hotel reservation management API built with FastAPI and PostgreSQL.

This project started as a command-line application using SQLite and was later refactored into a REST API using FastAPI and PostgreSQL as part of my backend development learning journey.

## Features

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

### Guests

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| GET    | `/guests`            | Get all guests    |
| POST   | `/guests`            | Create a guest    |
| GET    | `/guests/{guest_id}` | Get a guest by ID |
| PUT    | `/guests/{guest_id}` | Update a guest    |
| DELETE | `/guests/{guest_id}` | Delete a guest    |

### Rooms

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/rooms`           | Get all rooms       |
| POST   | `/rooms`           | Create a room       |
| GET    | `/rooms/available` | Get available rooms |
| GET    | `/rooms/{room_id}` | Get a room by ID    |
| PUT    | `/rooms/{room_id}` | Update a room       |
| DELETE | `/rooms/{room_id}` | Delete a room       |

### Reservations

| Method | Endpoint                                   | Description             |
| ------ | ------------------------------------------ | ----------------------- |
| GET    | `/reservations`                            | Get all reservations    |
| POST   | `/reservations`                            | Create a reservation    |
| GET    | `/reservations/{reservation_id}`           | Get reservation details |
| PUT    | `/reservations/{reservation_id}/cancel`    | Cancel reservation      |
| PUT    | `/reservations/{reservation_id}/check-in`  | Check in guest          |
| PUT    | `/reservations/{reservation_id}/check-out` | Check out guest         |

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* Pydantic
* Pytest

## Project Evolution

This project went through several iterations:

1. Started as a command-line hotel reservation application.
2. Used SQLite as the initial database.
3. Refactored into a layered architecture.
4. Migrated database storage from SQLite to PostgreSQL.
5. Converted the application into a FastAPI REST API.

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

## Running the Application

```bash
uvicorn main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
pytest
```

## Future Improvements

1. Expand FastAPI test coverage
2. Refactor database layer to SQLAlchemy ORM
3. JWT Authentication
4. Authorization
5. Role-based access control
6. Docker + Docker Compose
7. GitHub Actions (CI)
8. Deploy to Render
9. API rate limiting

```
```
