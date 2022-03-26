import asyncio
import os
from decimal import Decimal
from typing import Optional

from pydantic import condecimal
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Field, SQLModel, select


class Restaurant(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str
    currency: str


class MenuItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    price: condecimal(decimal_places=2)

    restaurant_id: Optional[int] = Field(default=None, foreign_key="restaurant.id")


async def main() -> None:
    db_url = os.environ.get("RESTAURANT_DB_URL", "sqlite+aiosqlite:///my_db")
    db_engine = create_async_engine(db_url)
    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(db_engine, expire_on_commit=False) as session:
        # Writing
        restaurant = Restaurant(
            name="Second best Pizza in town", address="Foo street 1", currency="EUR"
        )
        session.add(restaurant)
        await session.commit()

        pizza1 = MenuItem(name="Margherita", price=10.50, restaurant_id=restaurant.id)
        pizza2 = MenuItem(name="2xPineapple", price=16.80, restaurant_id=restaurant.id)
        session.add_all((pizza1, pizza2))
        await session.commit()

        # Reading
        query = (
            select(MenuItem)
            .join(Restaurant)
            .where(Restaurant.name == "Second best Pizza in town")
        )
        result = await session.execute(query)
        menu_items = result.scalars().all()

        assert len(menu_items) == 2
        assert menu_items[0] == MenuItem(
            id=1, name="Margherita", price=Decimal("10.50"), restaurant_id=restaurant.id
        )


if __name__ == "__main__":
    asyncio.run(main())
