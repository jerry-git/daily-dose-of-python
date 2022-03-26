import os
from decimal import Decimal
from typing import Optional

from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine, select


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


def main() -> None:
    db_url = os.environ.get("RESTAURANT_DB_URL", "sqlite:///my_db")
    db_engine = create_engine(db_url)
    SQLModel.metadata.create_all(db_engine)

    with Session(db_engine) as session:
        # Writing
        restaurant = Restaurant(
            name="Second best Pizza in town", address="Foo street 1", currency="EUR"
        )
        session.add(restaurant)
        session.commit()

        pizza1 = MenuItem(name="Margherita", price=10.50, restaurant_id=restaurant.id)
        pizza2 = MenuItem(name="2xPineapple", price=16.80, restaurant_id=restaurant.id)
        session.add_all((pizza1, pizza2))
        session.commit()

        # Reading
        query = (
            select(MenuItem)
            .join(Restaurant)
            .where(Restaurant.name == "Second best Pizza in town")
        )
        menu_items = session.exec(query).all()

        assert len(menu_items) == 2
        assert menu_items[0] == MenuItem(
            id=1, name="Margherita", price=Decimal("10.50"), restaurant_id=restaurant.id
        )


if __name__ == "__main__":
    main()
