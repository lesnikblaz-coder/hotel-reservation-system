from database import connection

ALLOWED_UPDATE_FIELDS = {
    "reservations": {
        "check_in_date",
        "check_out_date",
        "status"
    }
}

def create_reservations_table():
    connection.execute_query("""
    CREATE TABLE IF NOT EXISTS reservations(
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_id INTEGER,
        room_id INTEGER NOT NULL,
        check_in_date TEXT NOT NULL,
        check_out_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (guest_id) REFERENCES guests (guest_id) ON DELETE SET NULL,
        FOREIGN KEY (room_id) REFERENCES rooms (room_id)
    )
    """)

def db_reservation_insert(reservation):
    return connection.insert_query("""
    INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        reservation.guest_id,
        reservation.room_id,
        reservation.check_in_date,
        reservation.check_out_date,
        reservation.status
    ))

def db_reservation_delete(reservation_id):
    connection.execute_query("""
    DELETE FROM reservations
    WHERE reservation_id = ?
    """, (
        reservation_id,
    ))

def db_reservation_update(reservation_id, field, new_value):
    if field not in ALLOWED_UPDATE_FIELDS["reservations"]:
        raise ValueError("Invalid field.")

    query = f"""
    UPDATE reservations
    SET {field} = ?
    WHERE reservation_id = ?
    """

    connection.execute_query(query, (
        new_value,
        reservation_id
    ))

def db_get_reservations_all():
    return connection.fetch_query("""
    SELECT *
    FROM reservations
    ORDER BY reservation_id
    """)

def db_get_reservations_by_guest(guest_id):
    return connection.fetch_query("""
    SELECT *
    FROM reservations
    WHERE guest_id = ?
    """, (
        guest_id,
    ))

def db_get_reservation_by_id(reservation_id):
    return connection.fetch_query("""
    SELECT *
    FROM reservations
    WHERE reservation_id = ?
    """, (
        reservation_id,
    ), one=True)

def db_get_reservations_for_room(room_id):
    return connection.fetch_query("""
    SELECT *
    FROM reservations
    WHERE room_id = ?
    """, (
        room_id,
    ))

# conflict = existing check-out > new check-in AND  existing check-in < new check-out
def db_get_conflicting_reservation(room_id, new_check_in, new_check_out):
    return connection.fetch_query("""
    SELECT reservation_id 
    FROM reservations
    WHERE room_id = ?
        AND status NOT IN ('checked_out', 'cancelled')
        AND check_in_date < ?
        AND check_out_date > ?
    """,(
        room_id,
        new_check_out,
        new_check_in
    ),one=True)