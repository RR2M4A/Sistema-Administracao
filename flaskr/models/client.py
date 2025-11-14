from typing import List, Optional
from sqlalchemy import String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions import db


class Client(db.Model):
    """
    Represents the clients table in the database.

    Columns:
    - id: Unique primary key.
    - name: Client's name.
    - rg: General Registry (RG) of the client.
    - cpf: Individual Taxpayer Registry (CPF) of the client.
    - phone_number: Client's phone number.
    - birth_date: Client's date of birth.
    - entrances: Relationship with the client's entrances.
    """

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    rg: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[str] = mapped_column()

    entrances: Mapped[List['Entrance']] = relationship(     #type: ignore
        back_populates='client', cascade="all, delete-orphan")


    @classmethod
    def create(cls, name: str, rg: str, cpf: str, phone_number: str,
               birth_date: str) -> 'Client':
        """
        Instantiates a new Client object.
        The service layer is responsible for the database transaction.
        """

        return Client(
            name=name,
            rg=rg,
            cpf=cpf,
            phone_number=phone_number,
            birth_date=birth_date
        )


    @classmethod
    def find_by_id(cls, client_id: int) -> Optional['Client']:
        """Finds a client by their primary key (ID)."""
        return db.session.get(cls, client_id)


    @classmethod
    def find_by_cpf(cls, cpf: str) -> Optional['Client']:
        """Finds a client by their CPF."""

        return db.session.scalars(
            db.select(cls).where(cls.cpf == cpf)
        ).one_or_none()


    @classmethod
    def find_by_rg(cls, rg: str) -> Optional['Client']:
        """Finds a client by their RG."""

        return db.session.scalars(
            db.select(cls).where(cls.rg == rg)
        ).one_or_none()


    @classmethod
    def find_all(cls) -> List['Client']:
        """
        Returns all rows from the Client table, ordered by name.
        """

        return db.session.scalars(
            db.select(cls).order_by(cls.name)
        ).all()


    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of rows the Client table contains.
        """

        count_query = db.select(func.count(cls.id))
        total = db.session.scalar(count_query)
        return total or 0


    @classmethod
    def has_any(cls) -> bool:
        """Returns True if there is at least one client in the table."""

        first_client = db.session.scalars(db.select(cls)).first()
        return first_client is not None
