from models import Guest

def test_full_name():
    guest = Guest(
        first_name="Angie",
        last_name="Kwalss",
        email="angie@example.com",
        phone="1234567"
    )

    assert guest.full_name() == "Angie Kwalss"