from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UsersBase
from database import UsersRepository
from keyboards import inl_welcome


router = Router()


@router.message(CommandStart())
async def start(
    message: Message,
    session: AsyncSession
):
    user_repo = UsersRepository(
        session=session
    )

    user_entity = UsersBase(
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username
    )

    current_user = await user_repo.create(
        entity=user_entity
    )

    return await message.answer(
        'Добро пожаловать',
        reply_markup=inl_welcome.welcome
        )