from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UsersBase
from database import UsersRepository
from keyboards import inl_welcome
from middleware import ChatOnlyMiddleware


router = Router()
router.message.middleware(ChatOnlyMiddleware())


@router.message(CommandStart())
async def start(
    message: Message
):

    return await message.answer(
        'Добро пожаловать! Чтобы пользоваться ботом, добавьте его в свой чат или группу, назначте бота администратором и можете запускать бота по команде /start_group',
        reply_markup=inl_welcome.welcome
        )