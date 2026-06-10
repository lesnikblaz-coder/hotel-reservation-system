from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field, ConfigDict
from datetime import date
from decimal import Decimal

from exceptions import InvalidPhoneNumberError, ConflictingDateError, InvalidRoomNumberError

# --- shared validator ---
def validate_phone_number(phone: str | None) -> str | None:
    if phone is None:
        return phone

    phone = phone.replace(" ", "")

    if not ((phone.startswith("+") and phone[1:].isdigit()) or phone.isdigit()):
        raise InvalidPhoneNumberError("Invalid phone number.")

    return phone

def validate_dates(check_in_date: date, check_out_date: date) -> None:
    if check_out_date <= check_in_date:
        raise ConflictingDateError("Check-out must be after check in.")

    if check_in_date < date.today():
        raise ConflictingDateError("Check-in cannot be in the past.")

def validate_room_number(room_number: int) -> int | None:
    if room_number is None:
        return room_number

    if room_number <= 0:
        raise InvalidRoomNumberError("Room number must be positive.")

    return room_number

# --- input: creating a guest ---
class GuestCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=18)
    last_name: str = Field(min_length=2, max_length=23)
    email: EmailStr
    phone: str

    # validate phone number format
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

    # validate phone number format
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone):
        return validate_phone_number(phone)

# --- rooms ---
class RoomCreate(BaseModel):
    room_type: str
    room_number: int

    @field_validator("room_number")
    @classmethod
    def validate_room_num(cls, room_number):
        return validate_room_number(room_number)

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
    room_number: int | None = None
    capacity: int | None = Field(default = None, ge=2, le=12)
    price_per_night: float | None = Field(default = None, ge=99.99, le=1299.99)
    is_active: bool | None = None

    @field_validator("room_number")
    @classmethod
    def validate_room_num(cls, room_number):
        return validate_room_number(room_number)

# --- reservations ---
class ReservationCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date

    # validate date inputs
    @model_validator(mode="after")
    def validate_reservation_dates(self):
        validate_dates(self.check_in_date, self.check_out_date)
        return self

class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    status: str
    total_price: Decimal

class ReservationUpdate(BaseModel):
    guest_id: int | None = None
    room_id: int | None = None
    check_in_date: date | None = None
    check_out_date: date | None = None
    status: str | None = None
    # validate dates in reservation_services because only 1 might get updated.


# --- search available rooms by date range ---
class RoomAvailabilitySearch(BaseModel):
    check_in_date: date
    check_out_date: date
    capacity: int = 0

    @model_validator(mode="after")
    def validate_search_dates(self):
        validate_dates(self.check_in_date, self.check_out_date)
        return self

# --- revenue reports ---
class RevenueReportRequest(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_search_dates(self):
        if self.end_date <= self.start_date:
            raise ConflictingDateError("End date must be after start date.")
        return self

class RevenueReportResponse(BaseModel):
    revenue: Decimal

class MonthlyRevenueReportResponse(BaseModel):
    month: date
    revenue: Decimal

class YearlyRevenueReportResponse(BaseModel):
    year: date
    revenue: Decimal

class OccupancyReportResponse(BaseModel):
    total_rooms: int
    occupied_rooms: int
    occupancy_percentage: float

class OccupancyReportRequest(BaseModel):
    month_start: date
    month_end: date

    @model_validator(mode="after")
    def validate_search_dates(self):
        if self.month_end <= self.month_start:
            raise ConflictingDateError("End date must be after start date.")
        return self

class MonthlyOccupancyReportResponse(BaseModel):
    available_room_nights: int
    occupied_room_nights: int
    occupancy_percentage: float