def get_number(min_val, max_val):
    while True:
        try:
            number = int(input(f'Enter a number ({min_val}-{max_val}): '))
            if min_val <= number <= max_val:
                return number

            print(f'You must enter a number between {min_val} and {max_val}.')

        except ValueError:
            print("You must enter a number.")

def get_string_letters(prompt):
    while True:
        string = str(input(prompt))

        if not string.isalpha() or len(string) <= 1:
            print("Use only letters (min. 2).")
            continue

        return string

def get_string(prompt):
    while True:
        string = str(input(prompt)).strip()

        if string:
            return string

        print("Field cannot be empty. ")

def get_id():
    while True:
        try:
            id_input = int(input("Enter ID: "))

            if id_input > 0:
                return id_input

            print("Invalid ID.")

        except ValueError:
            print("You must enter a number.")

def get_fname():
    return get_string_letters("Enter first name: ")

def get_lname():
    return get_string_letters("Enter last name: ")

def get_email():
    return get_string("Enter email: ")

def get_phone():
    return get_string("Enter phone: ")

def get_field():
    return get_string("Enter field to update: ")

def print_valid_fields(object_):
    valid_fields = [
        field for field in vars(object_)
        if not field.endswith(("_id", "_number"))
           and field != "is_active"
    ]
    print("Valid fields: ", ", ".join(valid_fields))

def get_date(prompt):
    while True:
        string = str(input(prompt)).strip()

        if string:
            return string

        print("Field cannot be empty. ")

def objects_print(objects):
    if not objects:
        print("Nothing to display.")
        return
    for i, obj in enumerate(objects, 1):
        print(f'{i}. ---> {obj}')

def reservation_price(total_price):
    print(f'Total price of the reservation: ${total_price:,.2f}')