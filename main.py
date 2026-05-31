from database import guest_db, rooms_db, reservations_db

from reservation_system_app import ReservationSystem

def main():
    guest_db.create_guests_table()
    rooms_db.create_rooms_table()
    reservations_db.create_reservations_table()

    app = ReservationSystem()
    app.run()

if __name__ == "__main__":
    main()