from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict

from datetime import date

# --- shared validator ---
def validate_phone_number(phone: str | None) -> str | None:
    if phone is None:
        return phone

    phone = phone.replace(" ", "")

    if not ((phone.startswith("+") and phone[1:].isdigit()) or phone.isdigit()):
        raise ValueError("Invalid phone number.")

    return phone

# --- input: creating a guest ---
class GuestCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=18)
    last_name: str = Field(min_length=2, max_length=23)
    email: EmailStr
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        return validate_phone_number(phone)

# --- output: returning a guest ---
class GuestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guest_id: int
    first_name: str
    last_name: str
    email: str
    phone: str

# --- input: updating a guest (all optional) ---
class GuestUpdate(BaseModel):
    first_name: str | None = Field(default = None, min_length = 2, max_length = 18)
    last_name: str | None = Field(default = None, min_length = 2, max_length = 18)
    email: EmailStr | None = None
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        return validate_phone_number(phone)


# --- rooms ---
class RoomCreate(BaseModel):
    room_type: str

class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
    room_number: int
    room_type: str
    capacity: int
    price_per_night: float
    is_active: bool

class RoomUpdate(BaseModel):
    room_type: str | None = None
    capacity: int | None = Field(default = None, ge=2, le=12)
    price_per_night: float | None = Field(default = None, ge=99.99, le=1299.99)
    is_active: bool | None = None


# --- reservations ---
class ReservationCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date

class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    status: str

class ReservationUpdate(BaseModel):
    guest_id: int | None = None
    room_id: int | None = None
    check_in_date: date | None = None
    check_out_date: date | None = None
    status: str | None = None