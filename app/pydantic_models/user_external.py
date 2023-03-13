from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UserName(BaseModel):
    title: str
    first: str
    last: str


class LocationStreet(BaseModel):
    number: int
    name: str


class LocationCoordinates(BaseModel):
    latitude: str
    longitude: str


class LocationTimezone(BaseModel):
    offset: str
    description: str


class Location(BaseModel):
    street: LocationStreet
    city: str
    state: str
    country: str
    postcode: int | str
    coordinates: LocationCoordinates
    timezone: LocationTimezone


class Login(BaseModel):
    uuid: str
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str


class DateAndAgeField(BaseModel):
    date: datetime
    age: int


class Dob(DateAndAgeField): ...


class Registered(DateAndAgeField): ...


class Id(BaseModel):
    name: str
    value: str | None


class Picture(BaseModel):
    large: HttpUrl
    medium: HttpUrl
    thumbnail: HttpUrl


class ExternalUser(BaseModel):
    gender: str
    name: UserName
    location: Location
    email: str
    login: Login
    dob: Dob
    registered: Registered
    phone: str
    cell: str
    id: Id
    picture: Picture
    nat: str


class ExternalUserResponseInfo(BaseModel):
    seed: str
    results: int
    page: int
    version: str


class ExternalUserResponse(BaseModel):
    results: list[ExternalUser]
    info: ExternalUserResponseInfo
