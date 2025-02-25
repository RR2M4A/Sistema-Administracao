from typing import List
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Client(Base):

    """Classe que representará a TABLE com todos os clientes, ou seja,
    todas as pessoas que forem buscar os serviços da administração
    regional do gama.
    
    Suas colunas serão:
    
    .Id (chave única pra identificar a linha do banco de dados)
    .Nome do cliente
    .Registro geral (RG)
    .Cadastro de pessoa física (CPF)
    .Número de telefone
    .Data de nascimento
    .Entradas (lista de datas em que o cliente consultou a administração)
    """

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    rg: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(String(11))
    phone_number: Mapped[str] = mapped_column()
    birth_date: Mapped[Date] = mapped_column()

    entrances: Mapped[List["Entrance"]] = relationship(back_populates='client') 


class Entrance(Base):

    """Classe que representará a TABLE com as entradas de cada pessoa
    que consultou a administração regional do gama.
    
    Suas colunas serão:
    
    .Id (chave única pra identificar a linha do banco de dados)
    .Cliente (chave que relaciona a data a algum cliente)
    .Data de Entrada
    """

    __tablename__ = "entrances"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)

    client: Mapped["Client"] = relationship(back_populates='entrances') 
