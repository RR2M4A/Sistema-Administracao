from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from extensions import db
from utils import BRAZIL_TZ
from models import Client


DEPARTMENTS = {
    "COAG": "Coordenação de Administração Geral",
    "GEAD": "Gerência de Administração",
    "NUINF": "Núcleo de Informática",
    "NUMAP": "Núcleo de Material e Patrimônio",
    "GEOFIN": "Gerência de Orçamento e Finanças",
    "GEPES": "Gerência de Pessoas",
    "CODES": "Coordenação de Desenvolvimento",
    "DIDOT": "Diretoria de Desenvolvimento e Territorial",
    "GETEDEC": "Gerência de Gestão do Território e Desevolvimento Econômico",
    "DIART": "Diretoria de Articulação",
    "GEPSCEL": "Gerência de Políticas Sociais), Cultura), Esporte e Lazer",
    "COLOM": "Coordenação de Licenciamento), Obras e Manutenção",
    "DIALIC": "Diretoria de Aprovação e Licenciamento",
    "GELOAE": "Gerência de Licenciamento de Obras e Atividades Econômicas",
    "GEAPRO": "Gerência de Elaboração e Aprovação de Projetos",
    "DIROB": "Diretoria de Obras",
    "GEOB": "Gerência de Obras",
    "GEMAC": "Gerência de Manutenção e Conservação",
    "ASCOM": "Assessoria de comunicação",
    "ASTEC": "Assessoria Técnica",
    "ASPLAN": "Assessoria de Planejamento",
    "GAB": "Gabinete",
    "OUV": "Ouvidoria",
    "JSM": "Junta de Serviço Militar",
}

DEPARTMENT_KEYS = list(DEPARTMENTS.keys())
ALLOWED = ", ".join(f"'{k}'" for k in DEPARTMENT_KEYS)


class Entrance(db.Model):
    """
    Represents the entrances table in the database.

    Columns:
    - id: Unique primary key.
    - entrance: The timestamp of the entrance.
    - client_id: Foreign key linking to the client.
    - client: Relationship to the Client object.
    - department: The department in which the client has got into.
    """

    __tablename__ = "entrances"

    id: Mapped[int] = mapped_column(primary_key=True)
    entrance: Mapped[datetime] = mapped_column(nullable=False, index=True)
    department: Mapped[str] = mapped_column(nullable=False)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )

    client: Mapped["Client"] = relationship(back_populates='entrances')

    CheckConstraint(
        f"department IN ({ALLOWED})",
        name="check_department_valid"
    )


    @classmethod
    def create(cls, client: Client, department: str) -> 'Entrance':
        """
        Instantiates a new Entrance object for the given client.
        The service layer is responsible for the database transaction.
        """

        return Entrance(
            entrance=datetime.now(BRAZIL_TZ),
            client=client,
            department=department
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
