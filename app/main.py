from datetime import datetime
import itertools
import math

import asyncio
from fastapi import HTTPException, status


from app.base import app, engine, Session
from app.models import User as DbUser, UserLocation as DbUserLocation
from app.models.base import Model
from app.pydantic_models.user import User as PdUser, RequestUser
import aiohttp


from app.pydantic_models.user_external import ExternalUserResponse, ExternalUser


@app.get("/init")
async def init():
    print("dropping previosly-created")
    Model.metadata.drop_all(engine)
    print("creating tables...")
    Model.metadata.create_all(engine)
    print("tables created successfull")
    """
    Endpoint to reset database
    """
    return {"success": "Tables successfully recreated"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users() -> list[PdUser]:
    with Session() as session, session.begin():
        users: list[DbUser] = session.query(DbUser).all()
        return [PdUser.from_orm(user) for user in users]


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> PdUser:
    with Session() as session, session.begin():
        user = session.query(DbUser).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return PdUser.from_orm(user)


@app.post("/users/create")
async def create_user(user_data: RequestUser) -> PdUser:
    with Session() as session, session.begin():
        user_location = DbUserLocation(**user_data.location.dict())
        user = DbUser(
            location=user_location,
            **user_data.dict(exclude={"location"}),
        )
        session.add(user)
        session.flush()
        session.refresh(user)
        return PdUser.from_orm(user)
