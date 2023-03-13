from datetime import date

from pydantic import BaseModel


class UserLocation(BaseModel):
    street: str
    street_number: int
    city: str
    state: str
    country: str
    postcode: str


class User(BaseModel):
    id: int | None
    gender: str
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    birthday: date
    nationality: str
    cell: str
    location: UserLocation
