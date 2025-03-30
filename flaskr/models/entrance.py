from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions.database import db
from utils.date_utils import BRAZIL_TZ
from models.client import Client


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
        entrance = Entrance(
            entrance=datetime.now(BRAZIL_TZ),
            client=client
        )

        db.session.add(entrance)
        db.session.commit()
        return entrance
    

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