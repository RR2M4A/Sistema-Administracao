from typing import Optional, List
from sqlalchemy import exists
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash
from extensions.database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
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
    is_admin: Mapped[bool] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    is_blocked: Mapped[bool] = mapped_column()
    misses: Mapped[int] = mapped_column(default=0)
    

    @staticmethod
    def create(username: str, password_hash: str, 
               is_admin: bool, is_active: bool) -> 'User':
        """Instancia um objeto User e o armazena no banco de dados."""

        user = User(
            username = username,
            password_hash = password_hash,
            is_admin = is_admin,
            is_active = is_active,
            is_blocked = False
        )

        db.session.add(user)
        db.session.commit()
        return user


    @classmethod
    def has_any(cls) -> bool:
        """Retorna se existe ao menos uma tupla na table User."""

        return db.session.execute(
            db.select(exists().where(cls.id.isnot(None)))).scalar()
    

    @classmethod
    def find_by_id(cls, id: int) -> Optional['User']:
        """Busca um usuário pelo ID."""

        return db.session.execute(db.select(cls).where(
            cls.id==id)).scalar_one_or_none()
    

    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Busca um usuário pelo USERNAME."""

        return db.session.execute(db.select(cls).where(
            cls.username==username)).scalar_one_or_none()
    
    
    @classmethod
    def find_all(cls) -> List[Optional['User']]:
        """Retorna todas as linhas da table User, ordenadas pelo
        id."""

        return db.session.execute(
            db.select(cls).order_by(cls.id)).scalars().all()


    def check_password(self, password: str) -> bool:
        """Verifica se a senha inserida está correta."""

        return check_password_hash(self.password_hash, password)
