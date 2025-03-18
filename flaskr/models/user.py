from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash
from extensions.database import db


class User(db.Model):
    """Representa a tablea de usuários do sistema.
    
    Colunas:
    - id: Chave primária única para identificar a linha no banco de dados.
    - username: Usuário de login do sistema.
    - password: Senha de login.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)


    @classmethod
    def find_one(cls, username: str):
        return db.session.execute(db.select(cls).where(
            cls.username==username)).scalar_one_or_none()


    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)