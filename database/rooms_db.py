from database import connection

ALLOWED_UPDATE_FIELDS = {
    "rooms": {
        "room_type",
        "capacity",
        "price_per_night",
        "is_active"
    }
}

def create_rooms_table():
    # Create sequence starting at 1000
    connection.execute_query("""
    CREATE SEQUENCE IF NOT EXISTS room_number_seq
    START WITH 1000
    """)

    connection.execute_query("""
    CREATE TABLE IF NOT EXISTS rooms(
        room_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        room_number INTEGER UNIQUE NOT NULL DEFAULT nextval('room_number_seq'),
        room_type TEXT NOT NULL CHECK(
            room_type IN ('single', 'double', 'suite')
        ),
        capacity INTEGER NOT NULL,
        price_per_night REAL NOT NULL,
        is_active BOOLEAN NOT NULL
    )
    """) #is_active is a boolean so 0=False, 1=True

def db_room_insert(room):
    query = """
    INSERT INTO rooms (room_type, capacity, price_per_night, is_active)
    VALUES (%s, %s, %s, %s)
    RETURNING room_id, room_number
    """

    return connection.insert_query(query, (
        room.room_type,
        room.capacity,
        room.price_per_night,
        room.is_active
    ), more=True)

def db_room_delete(room_id):
    connection.execute_query("""
    DELETE FROM rooms
    WHERE room_id = %s
    """, (
        room_id,
    ))

def db_room_update(room_id, data):
    fields = []
    values = []

    if data.room_type is not None:
        fields.append("room_type = %s")
        values.append(data.room_type)

    if data.capacity is not None:
        fields.append("capacity = %s")
        values.append(data.capacity)

    if data.price_per_night is not None:
        fields.append("price_per_night = %s")
        values.append(data.price_per_night)

    if data.is_active is not None:
        fields.append("is_active = %s")
        values.append(data.is_active)

    values.append(room_id)

    if not fields:
        return

    query = f"""
    UPDATE rooms
    SET {", ".join(fields)}
    WHERE room_id = %s
    """

    connection.execute_query(query, tuple(values))

def db_get_rooms_all():
    return connection.fetch_query("""
    SELECT *
    FROM rooms
    ORDER BY room_id
    """)

def db_get_room_by_id(room_id):
    return connection.fetch_query("""
    SELECT *
    FROM rooms
    WHERE room_id = %s
    """, (
       room_id,
    ), one=True)

def db_get_available_rooms():
    return connection.fetch_query("""
    SELECT *
    FROM rooms
    WHERE is_active = True
    """)

def db_get_first_room_per_type():
    return connection.fetch_query("""
    SELECT *
    FROM rooms
    WHERE room_number IN (
          SELECT MIN(room_number)
          FROM rooms
          GROUP BY room_type
    )
    """)