from typing import List
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
    birth_date: Mapped[str] = mapped_column()

    entrances: Mapped[List["Entrance"]] = relationship(back_populates='client', cascade="all, delete-orphan")


    @classmethod
    def create(cls, data: dict):
        """Instancia um objeto cliente e o armazena no banco de dados."""

        client = Client(
            name=data["name"],
            rg=data["rg"],
            cpf=data["cpf"],
            phone_number=data["phone-number"],
            birth_date=data["birth-date"]
        )

        db.session.add(client)
        db.session.commit()
        return client
        

    @classmethod
    def find_one(cls, value: str, allowed_columns = ["cpf", "rg"]):
        """Busca e retorna um cliente do banco de dados."""

        for column in allowed_columns:
            client = db.session.execute(db.select(cls).where(
                getattr(cls, column) == value)).scalar_one_or_none()

            if client:
                return client


    @classmethod
    def find_all(cls):
        """Retorna todas as linhas da table."""

        return db.session.execute(db.select(cls)).scalars().all()