from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database import UsersRepository
from schemas import UsersBase


router = Router()


@router.message(Command('reg'))
async def reg(
    message: Message,
    session: AsyncSession
):
    user_repo = UsersRepository(
        session=session
    )

    new_user = await user_repo.create(
        entity=UsersBase(
            telegram_id=message.from_user.id,
            telegram_username='@'+message.from_user.username
        )
    )

    return await message.answer('ok')
