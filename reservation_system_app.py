from services import guest_services, room_services, reservation_services
from constants import VALID_ROOM_TYPES

import menu
import ui

class ReservationSystem:
    def __init__(self):
        self.active_guest = None

    def run(self):
        while True:
            if self.active_guest:
                print("\nACTIVE GUEST: ", self.active_guest.email, "\n")

            main_choice = menu.main_menu()

            if main_choice == 0:
                print("\n.........Exiting the program.........")
                break

            actions = {
                1: self.guest_section,
                2: self.room_section,
                3: self.reservation_section,
                #4: self.report_section
            }

            action = actions.get(main_choice)

            if action:
                action()
            else:
                print("Invalid choice.")

    def guest_section(self):
        second_choice = menu.guests_menu()

        guest_actions = {
            1: self.handle_guest_create,
            2: self.handle_guests_view,
            3: self.handle_guest_active,
            4: self.handle_guest_print_by_id,
            5: self.handle_guest_update,
            6: self.handle_guest_delete
        }

        action = guest_actions.get(second_choice)

        if action:
            action()

    def room_section(self):
        second_choice = menu.rooms_menu()

        room_actions = {
            1: self.handle_room_create,
            2: self.handle_rooms_view,
            3: self.handle_print_available_rooms,
            4: self.handle_room_update,
            5: self.handle_room_delete,
            6: self.handle_room_activate,
            7: self.handle_room_deactivate
        }

        action = room_actions.get(second_choice)

        if action:
            action()

    def reservation_section(self):
        second_choice = menu.reservations_menu()

        reservation_actions = {
            1: self.handle_reservation_create,
            2: self.handle_reservations_view,
            3: self.handle_reservation_cancel,
            4: self.handle_reservation_check_in,
            5: self.handle_reservation_check_out,
            6: self.handle_reservations_view_by_guest,
            7: self.handle_reservation_price
        }

        action = reservation_actions.get(second_choice)

        if action:
            action()

    """def report_section(self):
        second_choice = menu.reports_menu()

        report_actions = {
            # 1: self.handle_reports_occupied_rooms,
            # 2: self.handle_reports_available_rooms,
            # 3: self.handle_reports_most_booked_type,
            # 4: self.handle_reports_revenue_report
        }

        action = report_actions.get(second_choice)

        if action:
            action()"""

    # ------------------------------------

    # removing duplicated logic
    @staticmethod
    def ask_until_valid(input_func, validation_func):
        while True:
            value = input_func()
            try:
                validation_func(value)
                return value
            except ValueError as e:
                print(e)

    # ---------- GUESTS ----------
    def handle_guest_create(self):
        first_name = ui.get_fname()
        last_name = ui.get_lname()
        email = self.ask_until_valid(
            ui.get_email,
            guest_services.validate_email
        )
        phone = self.ask_until_valid(
            ui.get_phone,
            guest_services.validate_phone
        )

        created_guest = guest_services.guest_create(first_name, last_name, email, phone)
        print(f'Successfully created "{created_guest.full_name()}"')

    @staticmethod
    def handle_guests_view():
        guests = guest_services.guests_get_all()
        if not guests:
            print("No guests found.")
            return
        ui.objects_print(guests)

    def handle_guest_active(self):
        guest = self.handle_guest_find_by_id()
        self.active_guest = guest

    @staticmethod
    def handle_guest_find_by_id():
        search_id = ui.get_id()

        try:
            return guest_services.guest_select_by_id(search_id)

        except ValueError as e:
            print(e)
            return None

    def handle_guest_print_by_id(self):
        guest = self.handle_guest_find_by_id()
        if guest is not None:
            print(guest)

    def handle_guest_update(self):
        guest = self.handle_guest_find_by_id()

        if guest is None:
            return

        while True:
            field = ui.get_field()

            try:
                guest_services.validate_field(guest, field)
            except ValueError as e:
                print(e)
                ui.print_valid_fields(guest)
                continue

            new_value = ui.get_string("Enter new value: ")

            try:
                guest_services.guest_update(guest, field, new_value)
                break
            except ValueError as e:
                print(e)

        print("Successfully updated.")

    def handle_guest_delete(self):
        guest = self.handle_guest_find_by_id()

        if guest is None:
            return

        guest_services.guest_delete(guest)
        print(f'Successfully deleted "{guest.first_name}"')

    # ---------- ROOMS ----------
    @staticmethod
    def handle_room_create():
        while True:
            room_type = ui.get_string("Enter room type: ")

            try:
                room_services.room_create(room_type)
                break
            except ValueError as e:
                print(e)
                print(f'Valid room types: {", ".join(VALID_ROOM_TYPES.keys())}')
                continue

        print(f'Successfully created room - type: {room_type}')

    @staticmethod
    def handle_rooms_view():
        try:
            rooms = room_services.rooms_get_all()
            ui.objects_print(rooms)
        except ValueError as e:
            print(e)

    @staticmethod
    def handle_print_available_rooms():
        try:
            available_rooms = room_services.rooms_get_available()
            ui.objects_print(available_rooms)
        except ValueError as e:
            print(e)

    @staticmethod
    def handle_room_find_by_id():
        try:
            search_id = ui.get_id()
            return room_services.room_select_by_id(search_id)

        except ValueError as e:
            print(e)
            return None

    def handle_room_activate(self):
        room = self.handle_room_find_by_id()

        if room is None:
            return

        try:
            room_services.room_activate(room)
        except ValueError as e:
            print(e)

    def handle_room_deactivate(self):
        room = self.handle_room_find_by_id()

        if room is None:
            return

        try:
            room_services.room_deactivate(room)
        except ValueError as e:
            print(e)

    def handle_room_update(self):
        room = self.handle_room_find_by_id()

        if room is None:
            return

        while True:
            field = ui.get_field()

            try:
                room_services.validate_field(room, field)
            except ValueError as e:
                print(e)
                ui.print_valid_fields(room)
                continue

            new_value = ui.get_string("Enter new value: ")

            try:
                room_services.room_update(room, field, new_value)
                break
            except ValueError as e:
                print(e)

        print("Successfully updated.")

    def handle_room_delete(self):
        room = self.handle_room_find_by_id()

        if room is None:
            return

        room_services.room_delete(room)
        print(f'Successfully deleted room number: {room.room_number}')

    # ---------- RESERVATIONS ----------
    def handle_reservation_create(self):
        if not self.active_guest:
            print("Please select an active guest.")
            return

        print("Select room to book.")

        one_room_each_type = room_services.get_first_room_each_type()
        ui.objects_print(one_room_each_type)

        room = self.handle_room_find_by_id()
        if room is None:
            return

        while True:
            check_in = ui.get_date("Enter check-in date: ")
            check_out = ui.get_date("Enter check-out date: ")

            try:
                reservation_services.reservation_create(self.active_guest.guest_id, room.room_id, check_in, check_out)
                break
            except ValueError as e:
                print(e)
                continue

    @staticmethod
    def handle_reservations_view():
        reservations = reservation_services.reservations_get_all()
        if not reservations:
            print("No reservations found.")
            return
        ui.objects_print(reservations)

    def handle_reservation_cancel(self):
        if not self.active_guest:
            print("Please select an active guest.")
            return
        try:
            search_id = ui.get_id()
            reservation = reservation_services.reservation_select_by_id(search_id)
            reservation_services.reservation_cancel(self.active_guest.guest_id, reservation)
            print(f'Successfully canceled reservation: {reservation.reservation_id}')

        except ValueError as e:
            print(e)

    @staticmethod
    def handle_reservation_check_in():
        try:
            search_id = ui.get_id()
            reservation_services.reservation_check_in(search_id)
            print("Successfully checked in.")

        except ValueError as e:
            print(e)

    @staticmethod
    def handle_reservation_check_out():
        try:
            search_id = ui.get_id()
            reservation_services.reservation_check_out(search_id)
            print("Successfully checked out.")

        except ValueError as e:
            print(e)

    @staticmethod
    def handle_reservations_view_by_guest():
        try:
            search_id = ui.get_id()
            reservations = reservation_services.reservations_search_by_guest(search_id)
            ui.objects_print(reservations)

        except ValueError as e:
            print(e)

    @staticmethod
    def handle_reservation_price():
        try:
            search_id = ui.get_id()
            reservation = reservation_services.reservation_select_by_id(search_id)
            total_price = reservation_services.reservation_price(reservation.reservation_id)
            ui.reservation_price(total_price)

        except ValueError as e:
            print(e)