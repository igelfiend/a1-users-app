from datetime import date

from .base import NoExtraFieldsModel


class UserLocation(NoExtraFieldsModel):
    class Config:
        orm_mode = True

    street: str
    street_number: int
    city: str
    state: str
    country: str
    postcode: str


class RequestUser(NoExtraFieldsModel):
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


class RequestUpdateUserLocation(NoExtraFieldsModel):
    street: str | None
    street_number: int | None
    city: str | None
    state: str | None
    country: str | None
    postcode: str | None


class RequestUpdateUser(NoExtraFieldsModel):
    gender: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    birthday: date | None = None
    nationality: str | None = None
    cell: str | None = None
    location: RequestUpdateUserLocation | None = None
