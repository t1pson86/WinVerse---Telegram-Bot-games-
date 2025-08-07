from sqlalchemy import select
from typing import Optional

from database import db_conn
from schemas import GroupsBase
from database import GroupsModel


async def get_group_by_name(
    name: str
) -> Optional[GroupsBase]:
    async with db_conn.async_session() as session:
            
        result = await session.execute(
        select(GroupsModel)
        .where(GroupsModel.group_name=='@'+name)
        )

        current_group = result.scalars().first()

        return current_group
