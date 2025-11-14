from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions import db
from utils import BRAZIL_TZ
from models import Client


class Entrance(db.Model):
    """
    Represents the entrances table in the database.

    Columns:
    - id: Unique primary key.
    - entrance: The timestamp of the entrance.
    - client_id: Foreign key linking to the client.
    - client: Relationship to the Client object.
    """

    __tablename__ = "entrances"

    id: Mapped[int] = mapped_column(primary_key=True)
    entrance: Mapped[datetime] = mapped_column(nullable=False, index=True)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )

    client: Mapped["Client"] = relationship(back_populates='entrances')


    @classmethod
    def create(cls, client: Client) -> 'Entrance':
        """
        Instantiates a new Entrance object for the given client.
        The service layer is responsible for the database transaction.
        """

        return Entrance(
            entrance=datetime.now(BRAZIL_TZ),
            client=client
        )


    @classmethod
    def find_by_client(cls, client_id: int) -> List['Entrance']:
        """
        Finds all entrances for a specific client, ordered by most recent.
        """

        query = db.select(cls).where(
            cls.client_id == client_id
        ).order_by(cls.entrance.desc())

        return db.session.scalars(query).all()


    @classmethod
    def find_all(cls) -> List['Entrance']:
        """
        Returns all rows from the Entrance table, ordered by
        entrance datetime descending.
        """

        return db.session.scalars(
            db.select(cls).order_by(cls.entrance.desc())).all()


    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of rows the Entrance table contains,
        calculated efficiently by the database.
        """

        count_query = db.select(func.count(cls.id))
        total = db.session.scalar(count_query)

        return total or 0
