from fastapi import HTTPException, status

from app.base import Session, app
from app.models import User as DbUser
from app.models import UserLocation as DbUserLocation
from app.pydantic_models.user import RequestUpdateUser, RequestUser
from app.pydantic_models.user import User as PdUser


@app.get("/users")
async def get_users() -> list[PdUser]:
    with Session() as session, session.begin():
        users: list[DbUser] = session.query(DbUser).all()
        return [PdUser.from_orm(user) for user in users]


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> PdUser:
    with Session() as session, session.begin():
        user: DbUser = session.query(DbUser).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return PdUser.from_orm(user)


@app.post("/users/create", status_code=status.HTTP_201_CREATED)
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


@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_data: RequestUpdateUser) -> PdUser:
    with Session() as session, session.begin():
        user: DbUser = session.query(DbUser).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user.update(**user_data.dict(exclude_unset=True))
        session.add(user)
        return PdUser.from_orm(user)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with Session() as session, session.begin():
        user: DbUser = session.query(DbUser).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        session.delete(user)
        return {"deleted": user.id}
