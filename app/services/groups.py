from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.groups import GroupsBase
from app.database.models.groups import GroupsModel


class GroupsService():

    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_group(
        self,
        user_id: int,
        group: GroupsBase
    ) -> GroupsBase:
        
        result = await self.session.execute(
            select(GroupsModel)
            .where(GroupsModel.group_id==group.group_id)
            )

        current_group = result.scalars().first()

        if current_group is None:

            new_group = GroupsModel(
                group_id=group.group_id,
                group_name=group.group_name,
                user_id=user_id
            )

            self.session.add(new_group)
            await self.session.commit()

            return new_group
        
        
        return current_group
    

    async def get_group_by_id(
        self,
        id: int
    ):
        result = await self.session.execute(
            select(GroupsModel)
            .where(GroupsModel.group_id==id)
        )

        current_group = result.scalars().first()

        return current_group



