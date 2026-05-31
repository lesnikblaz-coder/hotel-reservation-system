from database import connection

ALLOWED_UPDATE_FIELDS = {
    "rooms": {
        "room_type",
        "capacity",
        "price_per_night",
        "is_active"
    }
}

ROOM_START_NUMBERS = {
    "single": 1000,
    "double": 2000,
    "suite": 3000
}

def generate_room_number(room_type):
    start = ROOM_START_NUMBERS[room_type]

    result = connection.fetch_query("""
    SELECT Max(room_number)
    FROM rooms
    WHERE room_type = ?
    """, (
        room_type,
    ), one=True )

    max_number = result[0]

    if max_number is None:
        return start

    return max_number + 1

def create_rooms_table():
    connection.execute_query("""
    CREATE TABLE IF NOT EXISTS rooms(
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number INTEGER UNIQUE NOT NULL,
        room_type TEXT NOT NULL CHECK(
            room_type IN ('single', 'double', 'suite')
        ),
        capacity INTEGER NOT NULL,
        price_per_night REAL NOT NULL,
        is_active INTEGER NOT NULL
    )
    """) #is_active is a boolean so 0=False, 1=True

def db_room_insert(room):
    room_number = generate_room_number(room.room_type)
    room.room_number = room_number

    query = """
    INSERT INTO rooms (room_number, room_type, capacity, price_per_night, is_active)
    VALUES (?, ?, ?, ?, ?)
    """

    return connection.insert_query(query, (
        room.room_number,
        room.room_type,
        room.capacity,
        room.price_per_night,
        room.is_active
    ))

def db_room_delete(room_id):
    connection.execute_query("""
    DELETE FROM rooms
    WHERE room_id = ?
    """, (
        room_id,
    ))

def db_room_update(room_id, data):
    fields = []
    values = []

    if data.room_type is not None:
        fields.append("room_type = ?")
        values.append(data.room_type)

    if data.capacity is not None:
        fields.append("capacity = ?")
        values.append(data.capacity)

    if data.price_per_night is not None:
        fields.append("price_per_night = ?")
        values.append(data.price_per_night)

    if data.is_active is not None:
        fields.append("is_active = ?")
        values.append(data.is_active)

    values.append(room_id)

    query = f"""
    UPDATE rooms
    SET {", ".join(fields)}
    WHERE room_id = ?
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
    WHERE room_id = ?
    """, (
       room_id,
    ), one=True)

def db_get_available_rooms():
    return connection.fetch_query("""
    SELECT *
    FROM rooms
    WHERE is_active = 1
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