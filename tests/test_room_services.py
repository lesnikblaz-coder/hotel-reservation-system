from hotel_reservation_system.services import room_services
from hotel_reservation_system import repository

def test_room_insert():
    room_services.room_create("single")
    room_services.room_create("single")
    room_services.room_create("double")
    room_services.room_create("suite")

    loaded_rooms = repository.get_all_rooms()

    assert len(loaded_rooms) == 4

    room_single1 = loaded_rooms[0]
    room_single2 = loaded_rooms[1]
    room_double = loaded_rooms[2]
    room_suite = loaded_rooms[3]

    assert room_single1.room_type == "single"
    assert room_single2.room_type == "single"
    assert room_double.room_type == "double"
    assert room_suite.room_type == "suite"

    print(f'\n\nTEST PrintSingle1: {room_single1}'
          f'\nTEST PrintSingle2: {room_single2}'
          f'\nTEST PrintDouble: {room_double}'
          f'\nTEST PrintSuite: {room_suite}'
          )