from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions import db
from utils import BRAZIL_TZ
from models import Client


class Entrance(db.Model):
    """Representa a tabela de entradas no banco de dados.

    Colunas:
    - id: Chave primária única para identificar a linha no banco de dados.
    - entrance_date: Data da entrada.
    - client_id: Chave estrangeira que relaciona esta entrada a um cliente.
    - client: Relacionamento com a classe Client, indicando o cliente que fez
    a entrada.
    """

    __tablename__ = "entrances"

    id: Mapped[int] = mapped_column(primary_key=True)
    entrance: Mapped[datetime] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)

    client: Mapped["Client"] = relationship(back_populates='entrances')


    @classmethod
    def create(cls, client: Client):
        """ Cria e retorna um objeto de Entrance."""
        entrance = Entrance(
            entrance=datetime.now(BRAZIL_TZ),
            client=client
        )

        db.session.add(entrance)
        db.session.commit()
        return entrance


    @staticmethod
    def findByClient(client_id: int):
        return Entrance.query.filter_by(client_id=client_id).all()


    @classmethod
    def find_all(cls) -> List:
        """Retorna todas as linhas da table Entrance, ordenadas pelo
        dia e horário de entrada de forma decrescente."""

        return db.session.execute(
            db.select(cls).order_by(cls.entrance.desc())).scalars().all()


    @classmethod
    def count(cls) -> int:
        """Retorna o total de linhas que a table Entrance contém."""

        return len(db.session.execute(db.select(cls)).all())
