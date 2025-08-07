from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..db import Base


class GroupsModel(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    group_id: Mapped[int] = mapped_column(nullable=True, default=None, unique=True)
    group_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    games: Mapped[str] = mapped_column(nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UsersModel"] = relationship(back_populates="groups")