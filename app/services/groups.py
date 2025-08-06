from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from schemas import GroupsBase
from database import GroupsModel

class GroupsService():

    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_group(
        self,
        user_id: int,
        group: GroupsBase
    ):
        result = await self.session.execute(
            select(GroupsModel)
            .where(GroupsModel.group_id==group.group_id)
            )

        group = result.scalars().first()

        if group is None:

            new_group = GroupsModel(
                group_id=group.group_id,
                group_name=group.group_name,
                user_id=user_id
            )

            self.session.execute(new_group)
            await self.session.commit()

            return new_group
        
        return group