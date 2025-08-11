from sqlalchemy import select, update, delete
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
    

    async def get_party_creator_by_user_id(
        self,
        creator_id: int
    ):
        result = await self.session.execute(
            select(PartiesModel)
            .where(PartiesModel.creator_id==creator_id)
        )

        current_party = result.scalars().first()

        return current_party
    

    async def get_party_opponent_by_user_id(
        self,
        opponent_id: int
    ):
        result = await self.session.execute(
            select(PartiesModel)
            .where(PartiesModel.opponent_id==opponent_id)
        )

        current_party = result.scalars().first()

        return current_party


    async def update_party_status(
        self,
        party_id: int,
        new_status: str
    ):
        
        result = await self.session.execute(
            update(PartiesModel)
            .where(PartiesModel.id==party_id)
            .values(status=new_status)
        )

        await self.session.commit()

        return result


    async def update_party_creator_info(
        self,
        creator_id: int,
        new_value: int
    ):

        result = await self.session.execute(
            update(PartiesModel)
            .where(PartiesModel.creator_id==creator_id)
            .values(creator_value=new_value)
        )

        await self.session.commit()

        return result
    

    async def update_party_opponent_info(
        self,
        opponent_id: int,
        new_value: int
    ):

        result = await self.session.execute(
            update(PartiesModel)
            .where(PartiesModel.opponent_id==opponent_id)
            .values(opponent_value=new_value)
        )

        await self.session.commit()
        return result
    

    async def delete_party(
        self,
        id: int
    ) -> None:
        
        result = await self.session.execute(
            delete(PartiesModel)
            .where(PartiesModel.id==id)
        )

        await self.session.commit()

        return None