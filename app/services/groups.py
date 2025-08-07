from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from schemas import GroupsBase
from database.models import GroupsModel, UsersModel


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
            .where(GroupsModel.group_name==group.group_name)
            )

        current_group = result.scalars().first()

        if current_group is None:

            new_group = GroupsModel(
                group_id=group.group_id,
                group_name=group.group_name,
                games=group.games,
                user_id=user_id
            )

            self.session.add(new_group)
            await self.session.commit()

            return new_group
        
        updt_user = await self.session.execute(
            update(UsersModel)
            .where(UsersModel.id==current_group.user_id)
            .values(creator=True)
        )

        self.session.commit(updt_user)
        self.session.refresh(updt_user)
        
        return current_group
    


    async def get_group_by_name(
        self,
        name: str
    ) -> Optional[GroupsBase]:
        
        result = await self.session.execute(
            select(GroupsModel)
            .where(GroupsModel.group_name==name)
        )

        current_group = result.scalars().first()

        return current_group


