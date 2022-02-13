import datetime as dt
import os

import motor
from beanie import Document, Indexed, PydanticObjectId, init_beanie, operators
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


class User(Document):
    name: Indexed(str)
    covid_vaccination_dates: list[dt.datetime] = []


async def init_db() -> None:
    db_uri = os.environ.get("VAX_APP_URI", "mongodb://localhost:27017")
    client = motor.motor_asyncio.AsyncIOMotorClient(db_uri)
    await init_beanie(database=client.db_name, document_models=[User])


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


class UserVaccinationRequest(BaseModel):
    vaccination_date: dt.datetime


@app.post("/users/{user_id}/covid-vaccination")
async def vaccinate_user(
    user_id: PydanticObjectId, request: UserVaccinationRequest
) -> Response:
    result = await User.find_one(User.id == user_id).update(
        operators.Push({User.covid_vaccination_dates: request.vaccination_date})
    )
    if not result.modified_count:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_201_CREATED)


#################
# Let's test it
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_it_stores_vaccinations_in_db() -> None:
    await init_db()
    user = await User(name="Jerry").insert()
    vaccination_dates = [
        dt.datetime(2021, 6, 14),
        dt.datetime(2021, 8, 11),
        dt.datetime(2022, 1, 14),
    ]

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        for d in vaccination_dates:
            response = await client.post(
                f"users/{user.id}/covid-vaccination",
                json={"vaccination_date": d.isoformat()},
            )
            assert response.status_code == status.HTTP_201_CREATED

    updated_user = await User.get(user.id)
    assert updated_user.covid_vaccination_dates == vaccination_dates
