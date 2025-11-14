from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash
from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Represents the system's user table.

    Columns:
    - id: Unique primary key.
    - username: User's login name.
    - password_hash: Hashed login password.
    - is_admin: Flag for administrator privileges.
    - is_active: Flag for active/enabled user.
    - misses: Counter for failed login attempts.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    misses: Mapped[int] = mapped_column(default=0)


    @classmethod
    def create(cls, username: str, password_hash: str,
               is_admin: bool = False) -> 'User':
        """
        Instantiates and returns a new User object.
        The service layer is responsible for the database transaction.
        """

        return cls(
            username=username,
            password_hash=password_hash,
            is_admin=is_admin,
        )


    @classmethod
    def has_any(cls) -> bool:
        """Returns True if there is at least one user in the table."""

        first_user = db.session.scalars(db.select(cls)).first()
        return first_user is not None


    @classmethod
    def find_by_id(cls, user_id: int) -> Optional['User']:
        """Finds a user by their primary key (ID)."""

        return db.session.get(cls, user_id)


    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Finds a user by their USERNAME."""

        return db.session.scalars(db.select(cls).where(
            cls.username == username)).one_or_none()


    @classmethod
    def find_all(cls) -> List['User']:
        """Returns all users, ordered by ID."""

        return db.session.scalars(
            db.select(cls).order_by(cls.id)).all()


    def check_password(self, password: str) -> bool:
        """Verifies if the provided password is correct."""

        return check_password_hash(self.password_hash, password)
