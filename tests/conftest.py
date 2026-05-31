import pytest
from hotel_reservation_system.database import guest_db, rooms_db, reservations_db, connection

@pytest.fixture(autouse=True)
def clean_db():
    guest_db.create_guests_table()
    rooms_db.create_rooms_table()
    reservations_db.create_reservations_table()

    connection.clear_reservations_table() #child first #also couldn't think of that myself
    connection.clear_rooms_table()
    connection.clear_guests_table()