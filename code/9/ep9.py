import datetime as dt
import random
from typing import Any

from dirty_equals import Contains, IsList, IsNow, IsPositiveFloat
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/order")
async def create_order() -> dict[str, Any]:
    # Just a dummy payload for demonstration
    return {
        "price": random.random() * 100,
        "products": ["milk", "coke", "pasta"],
        "created_at": dt.datetime.now().isoformat(),
        "created_by": "Jerry",
    }


def test_order_api() -> None:
    client = TestClient(app)

    response = client.post("/order")

    assert response.json() == {
        "price": IsPositiveFloat(),
        "products": IsList(length=3) & Contains("pasta"),
        "created_at": IsNow(iso_string=True),
        "created_by": "Jerry",
    }
