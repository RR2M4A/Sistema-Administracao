from typing import List
from datetime import datetime, date
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions.database import db


class Client(db.Model):
    """Representa a tabela de clientes do banco de dados.

    Colunas:
    - id: Chave primária única para identificar a linha no banco de dados.
    - name: Nome do cliente.
    - rg: Registro Geral (RG) do cliente.
    - cpf: Cadastro de Pessoa Física (CPF) do cliente.
    - phone_number: Número de telefone do cliente.
    - birth_date: Data de nascimento do cliente.
    - entrances: Relacionamento com as entradas realizadas pelo cliente, onde
    cada entrada é uma data em que o cliente consultou a administração.
    """

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    rg: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(String(11))
    phone_number: Mapped[str] = mapped_column()
    birth_date: Mapped[date] = mapped_column()

    entrances: Mapped[List["Entrance"]] = relationship(back_populates='client')


    @classmethod
    def create(cls, data: dict):
        client = Client(
            name=data["name"],
            rg=data["rg"],
            cpf=data["cpf"],
            phone_number=data["phone-number"],
            birth_date=datetime.strptime(data["birth-date"], "%d/%m/%Y")
        )

        db.session.add(client)
        db.session.commit()
        return client
        

    @classmethod
    def find_one(cls, cpf: str):
        return db.session.execute(db.select(cls).where(cls.cpf == cpf)).scalar_one_or_none()