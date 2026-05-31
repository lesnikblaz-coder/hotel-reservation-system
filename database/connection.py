import os
import psycopg2

from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

#HELPERS
def get_connection():
    conn = psycopg2.connect(host=os.getenv("DB_HOST"), dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), port=os.getenv("DB_PORT"))
    return conn

def execute_query(query: str, parameters: tuple=()):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, parameters)
        conn.commit()

def insert_query(query: str, parameters: tuple=(), more: bool = False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, parameters)

            if more:
                row = cursor.fetchone()
                inserted = {
                    "room_id": row[0],
                    "room_number": row[1]
                }

            else:
                inserted = cursor.fetchone()[0]

        conn.commit()
        return inserted

def fetch_query(query: str, parameters: tuple = (), one: bool = False):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parameters)

            return cursor.fetchone() if one else cursor.fetchall()

#TABLE CLEARING for testing
def clear_guests_table():
    execute_query("TRUNCATE TABLE guests RESTART IDENTITY CASCADE")

def clear_rooms_table():
    execute_query("TRUNCATE TABLE rooms RESTART IDENTITY CASCADE")

def clear_reservations_table():
    execute_query("TRUNCATE TABLE reservations RESTART IDENTITY CASCADE")

def drop_guests_table():
    execute_query("DROP TABLE IF EXISTS guests")

def drop_rooms_table():
    execute_query("DROP TABLE IF EXISTS rooms")

def drop_reservations_table():
    execute_query("DROP TABLE IF EXISTS reservations")