from typing import Optional

from .base_repository import BaseRepository
from schemas import GroupsBase
from ..db import get_new_async_session
from services import GroupsService

class GroupsRepository(BaseRepository[GroupsBase]):

    def __init__(self):
        self.session = get_new_async_session()
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

        return 'ok'


 
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