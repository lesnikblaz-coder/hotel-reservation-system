from database import guest_db, rooms_db, reservations_db
import models

#GUESTS
def _row_to_guest(row) -> models.Guest:
    return models.Guest(
        guest_id=row["guest_id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        email=row["email"],
        phone=row["phone"]
    )

def get_all_guests() -> list[models.Guest]:
    rows = guest_db.db_get_guest_all()
    return [_row_to_guest(row) for row in rows]

def get_guest_by_id(guest_id) -> models.Guest | None:
    row = guest_db.db_get_guest_by_id(guest_id)
    return _row_to_guest(row) if row else None

def get_guest_by_email(email) -> models.Guest | None:
    row = guest_db.db_get_guest_by_email(email)
    return _row_to_guest(row) if row else None

def get_guest_by_phone(phone) -> models.Guest | None:
    row = guest_db.db_get_guest_by_phone(phone)
    return _row_to_guest(row) if row else None

def guest_create(guest):
    return guest_db.db_guest_insert(guest)

def guest_delete(guest_id):
    return guest_db.db_guest_delete(guest_id)

def guest_update(guest_id, data):
    return guest_db.db_guest_update(guest_id, data)

#ROOMS
def _row_to_room(row) -> models.Room:
    return models.Room(
        room_id=row["room_id"],
        room_number=row["room_number"],
        room_type=row["room_type"],
        capacity=row["capacity"],
        price_per_night=row["price_per_night"],
        is_active=row["is_active"]
    )

def get_all_rooms() -> list[models.Room]:
    rows = rooms_db.db_get_rooms_all()
    return [_row_to_room(row) for row in rows]

def get_room_by_id(room_id) -> models.Room | None:
    row = rooms_db.db_get_room_by_id(room_id)
    return _row_to_room(row) if row else None

def room_create(room):
    return rooms_db.db_room_insert(room)

def room_delete(room_id):
    return rooms_db.db_room_delete(room_id)

def room_update(room_id, data):
    return rooms_db.db_room_update(room_id, data)

def get_available_rooms():
    rows = rooms_db.db_get_available_rooms()
    return [_row_to_room(row) for row in rows]

def get_first_room_per_type():
    rows = rooms_db.db_get_first_room_per_type()
    return [_row_to_room(row) for row in rows]

#RESERVATIONS
def _row_to_reservation(row) -> models.Reservation:
    return models.Reservation(
        reservation_id=row["reservation_id"],
        guest_id=row["guest_id"],
        room_id=row["room_id"],
        check_in_date=row["check_in_date"],
        check_out_date=row["check_out_date"],
        status=row["status"]
    )

def get_all_reservations() -> list[models.Reservation]:
    rows = reservations_db.db_get_reservations_all()
    return [_row_to_reservation(row) for row in rows]

def get_reservation_by_guest(guest_id) -> list[models.Reservation]:
    rows = reservations_db.db_get_reservations_by_guest(guest_id)
    return [_row_to_reservation(row) for row in rows]

def reservation_create(reservation):
    return reservations_db.db_reservation_insert(reservation)

def get_conflicting_reservations(room_id, check_in_date, check_out_date):
    return reservations_db.db_get_conflicting_reservation(room_id, check_in_date, check_out_date)

def get_reservation_by_id(reservation_id):
    row = reservations_db.db_get_reservation_by_id(reservation_id)
    return _row_to_reservation(row) if row else None

def get_reservations_for_room(room_id):
    rows = reservations_db.db_get_reservations_for_room(room_id)
    return [_row_to_reservation(row) for row in rows]

def reservation_update(reservation_id, field, new_value):
    return reservations_db.db_reservation_update(reservation_id, field, new_value)