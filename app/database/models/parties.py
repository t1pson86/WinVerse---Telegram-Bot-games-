from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base

class PartiesModel(Base):
    __tablename__ = 'parties'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    game_type: Mapped[str] = mapped_column(nullable=False)    

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    opponent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    creator_value: Mapped[int] = mapped_column(nullable=True, default=None)
    opponent_value: Mapped[int] = mapped_column(nullable=True, default=None)

    creator: Mapped["UsersModel"] = relationship(foreign_keys=[creator_id])
    opponent: Mapped["UsersModel"] = relationship(foreign_keys=[opponent_id])