from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base_repository import BaseRepository
from schemas import PartiesBase
from services import PartiesService

class PartiesRepository(BaseRepository[PartiesBase]):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.partie_service = PartiesService(
            session = self.session
        )


    async def create(
        self, 
        entity: PartiesBase
    ) -> PartiesBase:

        return await self.partie_service.add_party(
            party=entity
        )

 
    async def read(
        self, 
        id: int
    ) -> Optional[PartiesBase]:

        return await self.partie_service.get_party_id(
            id=id
        )


 
    async def update(
        self, 
        party_id: int,
        new_status: str
    ) -> PartiesBase:

        return await self.partie_service.update_party_status(
            party_id=party_id,
            new_status=new_status
        )



    async def delete(
        self, 
        id: int
    ) -> None:

        return await self.partie_service.delete_party(
            id=id
        )
    

    async def get_party_by_creator_id(
        self,
        creator_id: int
    ):
        
        return await self.partie_service.get_party_creator_by_user_id(
            creator_id=creator_id
        )
    

    async def get_party_by_opponent_id(
        self,
        opponent_id: int
    ):
        
        return await self.partie_service.get_party_opponent_by_user_id(
            opponent_id=opponent_id
        )


    async def update_party_info_by_creator_id(
        self,
        creator_id: int,
        new_value: int
    ):
        
        return await self.partie_service.update_party_creator_info(
            creator_id=creator_id,
            new_value=new_value
        )


    async def update_party_info_by_opponent_id(
        self,
        opponent_id: int,
        new_value: int
    ):
        
        return await self.partie_service.update_party_opponent_info(
            opponent_id=opponent_id,
            new_value=new_value
        )