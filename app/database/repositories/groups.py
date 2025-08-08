from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repository import BaseRepository
from schemas import GroupsBase
from services import GroupsService

class GroupsRepository(BaseRepository[GroupsBase]):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.group_service = GroupsService(
            session=self.session
        )


    async def create(
        self, 
        user_id: int,
        entity: GroupsBase
    ) -> GroupsBase:

        return await self.group_service.add_group(
            user_id=user_id,
            group=entity
        )


 
    async def read(
        self, 
        id: int
    ) -> Optional[GroupsBase]:

        return await self.group_service.get_group_by_id(
            id = id
        )


 
    async def update(
        self, 
        entity: GroupsBase
    ) -> GroupsBase:

        return 'ok'



    async def delete(
        self, 
        id: int
    ) -> None:

        return 'ok'
    