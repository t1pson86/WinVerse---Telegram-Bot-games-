from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    telegram_username: Mapped[str] = mapped_column(nullable=False)
    