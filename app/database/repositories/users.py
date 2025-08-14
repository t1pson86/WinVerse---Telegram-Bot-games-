from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base_repository import BaseRepository
from app.schemas.users import UsersBase
from app.services.users import UsersService

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
    
    
    async def get_by_name(
        self,
        name: str
    ) -> Optional[UsersBase]:
        
        return await self.user_service.get_user_by_name(
            name=name
        )
    
    
    async def get_by_telegram_id(
        self,
        telegram_id: int
    ) -> Optional[UsersBase]:
        
        return await self.user_service.get_user_by_telegram_id(
            telegram_id=telegram_id
        )