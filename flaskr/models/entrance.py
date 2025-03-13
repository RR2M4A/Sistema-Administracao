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