from typing import Any

from quart import Quart, request

app = Quart(__name__)


@app.post("/my-endpoint")
async def my_endpoint() -> dict[str, Any]:
    request_json = await request.get_json()
    return {"echoed data": request_json}


#######################################
# Let's test it
import pytest


@pytest.mark.asyncio
async def test_my_endpoint() -> None:
    client = app.test_client()

    response = await client.post("/my-endpoint", json={"foo": "bar"})

    assert response.status_code == 200
    response_data = await response.get_json()
    assert response_data == {"echoed data": {"foo": "bar"}}
