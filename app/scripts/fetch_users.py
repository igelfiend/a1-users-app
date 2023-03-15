import csv
import itertools
import math
import sys

import aiohttp
import asyncio
from tenacity import retry, wait_fixed, stop_after_attempt

from app.pydantic_models.user import (
    RequestUser as PdUser,
    UserLocation as PdUserLocation,
)
from app.pydantic_models.user_external import ExternalUserResponse, ExternalUser
from app.base import Session
from app.models import User as DbUser, UserLocation as DbUserLocation


response_mock = """
{
    "results": [
        {
            "gender": "male",
            "name": {"title": "Mr", "first": "Janko", "last": "Dokić"},
            "location": {
                "street": {"number": 5103, "name": "Vinogradarska"},
                "city": "Sečanj",
                "state": "Jablanica",
                "country": "Serbia",
                "postcode": 48983,
                "coordinates": {"latitude": "63.3861", "longitude": "-18.8406"},
                "timezone": {"offset": "-3:30", "description": "Newfoundland"}
            },
            "email": "janko.dokic@example.com",
            "login": {
                "uuid": "5258eb16-1033-4c4f-8303-adb138a3afc0",
                "username": "angryelephant683",
                "password": "chilli",
                "salt": "hampUp9q",
                "md5": "be064c3a2557a605978ed2077b220f35",
                "sha1": "5b48b863a45d91a74d89ccb31599852eda5e8704",
                "sha256": "372ef0d7e52e0f0262b4e24c0a39549e0750fae27b5d9336bf943ead7b576d9b"
            },
            "dob": {"date": "1993-08-27T05:36:54.602Z", "age": 29},
            "registered": {"date": "2016-09-17T17:25:19.177Z", "age": 6},
            "phone": "015-6269-704",
            "cell": "063-3455-035",
            "id": {"name": "SID", "value": "426656732"},
            "picture": {
                "large": "https://randomuser.me/api/portraits/men/9.jpg",
                "medium": "https://randomuser.me/api/portraits/med/men/9.jpg",
                "thumbnail": "https://randomuser.me/api/portraits/thumb/men/9.jpg"
            },
            "nat": "RS"
        }
    ],
    "info": {"seed": "2323a41007d4dd6f", "results": 1, "page": 1, "version": "1.4"}
}
"""

MAX_RETRY_COUNT = 5
RETRY_WAIT = 1

MOCK = False


@retry(wait=wait_fixed(RETRY_WAIT), stop=stop_after_attempt(MAX_RETRY_COUNT))
async def get_external_user_data_from_url(url: str, session: aiohttp.ClientSession):
    if MOCK:
        from copy import copy

        return copy(response_mock)
    else:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.text()
            print(f"status: {response.status}")
            print(f"reason: {response.reason}")
            return data


async def fetch_user_data(url: str, users_count: int) -> dict:
    external_users: list[ExternalUser] = []
    async with aiohttp.ClientSession() as session:
        for _ in range(users_count):
            data = await get_external_user_data_from_url(url, session)
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


async def get_external_users_data(url: str, users_count: int, workers_count: int):
    workers_args = get_workers_args(
        url=url,
        workers_count=workers_count,
        users_count=users_count,
    )

    results = await asyncio.gather(
        *[fetch_user_data(**worker_args) for worker_args in workers_args],
    )
    return itertools.chain(*results)


def get_nationality_names(path: str) -> dict:
    with open(path, "r") as file:
        data = csv.reader(file, delimiter=",")
        return {key: value for value, key in data}


def convert_external_user_to_local(
    ext_users: list[ExternalUser],
    nationality_map: dict[str, str],
) -> list[PdUser]:
    users: list[PdUser] = []
    for ext_user in ext_users:
        user = PdUser(
            gender=ext_user.gender,
            first_name=ext_user.name.first,
            last_name=ext_user.name.last,
            email=ext_user.email,
            username=ext_user.login.username,
            password=ext_user.login.password,
            birthday=ext_user.dob.date.date(),
            nationality=nationality_map.get(ext_user.location.country, "unknown"),
            cell=ext_user.cell,
            location=PdUserLocation(
                street=ext_user.location.street.name,
                street_number=ext_user.location.street.number,
                city=ext_user.location.city,
                state=ext_user.location.state,
                country=ext_user.location.country,
                postcode=ext_user.location.postcode,
            ),
        )
        users.append(user)

    return users


if __name__ == "__main__":
    url = "https://randomuser.me/api/"
    users_count = sys.argv[1] if len(sys.argv) > 1 else 10
    workers_count = sys.argv[2] if len(sys.argv) > 2 else 1
    ext_users = asyncio.run(
        get_external_users_data(
            url=url,
            users_count=users_count,
            workers_count=workers_count,
        ),
    )

    nationality_map = get_nationality_names("./app/static/demonyms.csv")
    users = convert_external_user_to_local(
        ext_users=ext_users,
        nationality_map=nationality_map,
    )

    print(f"received and parsed {len(list(users))} users")

    with Session() as session, session.begin():
        db_users = []
        for user in users:
            print(f"user: {user.dict()}")
            user_location = DbUserLocation(**user.location.dict(exclude={"id"}))
            session.add(user_location)
            db_user = DbUser(
                location=user_location,
                **user.dict(
                    exclude={
                        "id",
                        "location",
                    }
                ),
            )
            session.add(db_user)
            db_users.append(db_user)

    print(f"Database updated")
