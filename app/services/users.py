from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UsersBase
from database.models import UsersModel


class UsersService():

    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_user(
        self,
        user: UsersBase
    ):
        res = await self.session.execute(
            select(UsersModel)
            .where(UsersModel.telegram_id==user.telegram_id)
            )

        current_user = res.scalars().first()


        if current_user is None:
            new_user = UsersModel(
                telegram_id = user.telegram_id,
                telegram_username = user.telegram_username,
                creator=True
            )

            self.session.add(new_user)
            await self.session.commit()

            return new_user

        return current_user