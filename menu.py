import ui

def main_menu():
    print("===== HOTEL RESERVATION SYSTEM =====\n")
    print("1. Guests")
    print("2. Rooms")
    print("3. Reservations")
    print("4. Reports")
    print("0. Exit")

    choice = ui.get_number(0, 4)
    return choice

def guests_menu():
    print("===== GUESTS =====\n")
    print("1. Create guest")
    print("2. View guests")
    print("3. Select active guest")
    print("4. Find guest by ID")
    print("5. Update guest")
    print("6. Delete guest")
    print("0. Back")

    choice = ui.get_number(0, 6)
    return choice

def rooms_menu():
    print("===== ROOMS =====\n")
    print("1. Create room")
    print("2. View rooms")
    print("3. Search available rooms")
    print("4. Update room")
    print("5. Delete room")
    print("6. Activate room")
    print("7. Deactivate room")
    print("0. Back")

    choice = ui.get_number(0, 7)
    return choice

def reservations_menu():
    print("===== RESERVATIONS =====\n")
    print("1. Create reservation")
    print("2. View reservations")
    print("3. Cancel reservation")
    print("4. Check in guest")
    print("5. Check out guest")
    print("6. View guest reservations")
    print("7. Reservation price")
    print("0. Back")

    choice = ui.get_number(0, 7)
    return choice

def reports_menu():
    print("===== REPORTS =====\n")
    print("1. Rooms currently occupied")
    print("2. Available rooms")
    print("3. Most booked room type")
    print("4. Revenue report")
    print("0. Back")

    choice = ui.get_number(0, 4)
    return choice