from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database.models import PartiesModel
from schemas import PartiesBase

class PartiesService():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_party(
        self,
        party: PartiesBase
    ) -> PartiesBase:
        
        result = await self.session.execute(
            select(PartiesModel)
            .where(PartiesModel.creator_id==party.creator_id)
        )

        current_party = result.scalars().first()

        if current_party is None:

            new_party = PartiesModel(
                game_type=party.game_type,
                creator_id=party.creator_id,
                opponent_id=party.opponent_id
            )

            self.session.add(new_party)
            await self.session.commit()
            await self.session.refresh(new_party)

            return new_party
        
        return current_party
    
    

    async def get_party_id(
        self,
        id: int
    ) -> Optional[PartiesBase]:
        
        result = await self.session.execute(
            select(PartiesModel)
            .where(PartiesModel.id==id)
        )

        current_party = result.scalars().first()

        return current_party