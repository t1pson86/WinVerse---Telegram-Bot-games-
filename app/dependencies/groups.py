from sqlalchemy import select
from typing import Optional

from database import db_conn
from schemas import GroupsBase
from database import UsersModel


async def get_user_by_id(
    id: int
) -> Optional[GroupsBase]:
    async with db_conn.async_session() as session:
            
        result = await session.execute(
            select(UsersModel)
            .where(UsersModel.telegram_id==id)
            )

        current_group = result.scalars().first()

        return current_group
