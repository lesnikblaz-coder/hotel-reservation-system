from database import connection

def create_guests_table():
    connection.execute_query("""
    CREATE TABLE IF NOT EXISTS guests(
        guest_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    )
    """)

def db_guest_insert(guest):
    query = """
    INSERT INTO guests (first_name, last_name, email, phone)
    VALUES (%s, %s, %s, %s)
    RETURNING guest_id
    """

    return connection.insert_query(query, (
        guest.first_name,
        guest.last_name,
        guest.email,
        guest.phone
    ))

def db_guest_delete(guest_id):
    connection.execute_query("""
    DELETE FROM guests
    WHERE guest_id = %s
    """, (
        guest_id,
    ))

def db_guest_update(guest_id, data):
    fields = []
    values = []

    if data.first_name is not None:
        fields.append("first_name = %s")
        values.append(data.first_name)

    if data.last_name is not None:
        fields.append("last_name = %s")
        values.append(data.last_name)

    if data.email is not None:
        fields.append("email = %s")
        values.append(data.email)

    if data.phone is not None:
        fields.append("phone = %s")
        values.append(data.phone)

    values.append(guest_id)

    if not fields:
        return

    query = f"""
    UPDATE guests
    SET {", ".join(fields)}
    WHERE guest_id = %s
    """

    connection.execute_query(query, tuple(values))

def db_get_guest_all():
    return connection.fetch_query("""
    SELECT *
    FROM guests
    ORDER BY guest_id
    """)

def db_get_guest_by_id(guest_id):
    return connection.fetch_query("""
    SELECT *
    FROM guests
    WHERE guest_id = %s
    """, (
        guest_id,
    ), one=True)

def db_get_guest_by_email(email):
    return connection.fetch_query("""
    SELECT *
    FROM guests
    WHERE email = %s
    """, (
        email,
    ), one=True)

def db_get_guest_by_phone(phone):
    return connection.fetch_query("""
    SELECT *
    from guests
    WHERE phone = %s
    """, (
       phone,
    ), one=True)