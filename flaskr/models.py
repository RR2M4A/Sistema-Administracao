from typing import List
from datetime import date
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import db


class User(db.Model):

    """Esta classe representa os usuários do sistema.
    
    Colunas:
    - id: Chave primária única para identificar a linha no banco de dados.
    - username: Usuário de login do sistema.
    - password: Senha de login.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)



class Client(db.Model):

    """Classe que representa a tabela de clientes. Cada instância da classe
    corresponderá a um cliente que consultou a administração regional do Gama.

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


class Entrance(db.Model):

    """Classe que representa a tabela de entradas. Cada instância da classe
    corresponde a uma entrada de um cliente na administração regional do Gama.

    Colunas:
    - id: Chave primária única para identificar a linha no banco de dados.
    - entrance_date: Data da entrada.
    - client_id: Chave estrangeira que relaciona esta entrada a um cliente.
    - client: Relacionamento com a classe Client, indicando o cliente que fez
    a entrada.
    """

    __tablename__ = "entrances"

    id: Mapped[int] = mapped_column(primary_key=True)
    entrance_date: Mapped[date] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)

    client: Mapped["Client"] = relationship(back_populates='entrances')
