from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import UsersModel

router = Router()

@router.message(CommandStart())
async def start(
    message: Message,
    session: AsyncSession
):
    res = await session.execute(
        select(UsersModel)
        .where(UsersModel.telegram_id==message.from_user.id)
        )

    user = res.scalars().first()


    if user is None:
        new_user = UsersModel(
            telegram_id = message.from_user.id,
            telegram_username = message.from_user.username
        )

        session.add(new_user)
        await session.commit()

    return await message.answer('Добро пожаловать!')