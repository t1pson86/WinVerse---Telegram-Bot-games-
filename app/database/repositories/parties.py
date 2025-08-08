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

        return 'ok'


 
    async def update(
        self, 
        entity: PartiesBase
    ) -> PartiesBase:

        return 'ok'



    async def delete(
        self, 
        id: int
    ) -> None:

        return 'ok'
    
