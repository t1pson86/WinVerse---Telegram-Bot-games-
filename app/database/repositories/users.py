from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base_repository import BaseRepository
from schemas import UsersBase
from services import UsersService

class UsersRepository(BaseRepository[UsersBase]):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UsersService(
            session = self.session
        )


    async def create(
        self, 
        entity: UsersBase
    ) -> UsersBase:

        return await self.user_service.add_user(
            user=entity
        )


 
    async def read(
        self, 
        id: int
    ) -> Optional[UsersBase]:

        return 'ok'


 
    async def update(
        self, 
        entity: UsersBase
    ) -> UsersBase:

        return 'ok'



    async def delete(
        self, 
        id: int
    ) -> None:

        return 'ok'