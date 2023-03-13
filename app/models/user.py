from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model


class UserLocation(Model):
    __tablename__ = "userlocations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street = Column(String(100))
    street_number = Column(Integer)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postcode = Column(String(20))
    user: Mapped["User"] = relationship(back_populates="location", passive_deletes=True)


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    username = Column(String(100))
    password = Column(String(30))
    birthday = Column(Date)
    nationality = Column(String(50))
    cell = Column(String(50))
    location_id: Mapped[id] = mapped_column(
        ForeignKey(
            "userlocations.id",
            ondelete="CASCADE",
        ),
    )
    location: Mapped[UserLocation] = relationship(back_populates="user")
