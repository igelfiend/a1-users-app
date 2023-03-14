from datetime import date

from pydantic import BaseModel


class UserLocation(BaseModel):
    class Config:
        orm_mode = True

    street: str
    street_number: int
    city: str
    state: str
    country: str
    postcode: str


class RequestUser(BaseModel):
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


class User(RequestUser):
    class Config:
        orm_mode = True

    id: int
