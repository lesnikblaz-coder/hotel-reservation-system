import sqlite3

DB_NAME = "hotel_reservation_system.db"

#HELPERS
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def execute_query(query: str, parameters: tuple=()):
    with get_connection() as conn:
        conn.execute(query, parameters)

def insert_query(query: str, parameters: tuple=()):
    with get_connection() as conn:
        cursor = conn.execute(query, parameters)
        return cursor.lastrowid

def fetch_query(query: str, parameters: tuple = (), one: bool = False):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query, parameters)

        return cursor.fetchone() if one else cursor.fetchall()

#TABLE CLEARING for testing
def clear_guests_table():
    execute_query("DELETE FROM guests")
    execute_query("DELETE FROM sqlite_sequence WHERE name='guests'") #resets the ID to 1 for testing

def clear_rooms_table():
    execute_query("DELETE FROM rooms")
    execute_query("DELETE FROM sqlite_sequence WHERE name='rooms'")

def clear_reservations_table():
    execute_query("DELETE FROM reservations")
    execute_query("DELETE FROM sqlite_sequence WHERE name='reservations'")

def drop_guests_table():
    execute_query("DROP TABLE guests")

def drop_rooms_table():
    execute_query("DROP TABLE rooms")

def drop_reservations_table():
    execute_query("DROP TABLE reservations")