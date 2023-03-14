from datetime import datetime
import itertools
import math

import asyncio
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.base import app, engine, Session
from app.models.base import Model
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


async def fetch_user_data(url: str, users_count: int) -> dict:
    external_users: list[ExternalUser] = []
    async with aiohttp.ClientSession() as session:
        for _ in range(users_count):
            async with session.get(url) as response:
                data = await response.text()
            external_users.append(ExternalUserResponse.parse_raw(data).results[0])
    return external_users


def get_workers_args(url: str, workers_count: int, users_count: int):
    users_for_worker = math.ceil(users_count / workers_count)

    workers_args = [
        {"url": url, "users_count": users_for_worker} for _ in range(workers_count - 1)
    ]
    users_for_last_worker = users_count - users_for_worker * (workers_count - 1)
    workers_args.append({"url": url, "users_count": users_for_last_worker})
    return workers_args


async def get_external_users_data(url: str, users_count: int):
    workers_count = 5

    workers_args = get_workers_args(
        url=url,
        workers_count=workers_count,
        users_count=users_count,
    )

    results = await asyncio.gather(
        *[fetch_user_data(**worker_args) for worker_args in workers_args],
    )
    return itertools.chain(*results)


@app.get("/")
async def root():
    global calls_counter
    calls_counter = 0
    print("requesting user info")
    url = "https://randomuser.me/api/"
    users_count = 100

    users = await get_external_users_data(url=url, users_count=users_count)

    print(f"received and parsed {len(list(users))} users")

    return {"message": "Hello World"}
