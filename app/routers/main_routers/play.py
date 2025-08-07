from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from middleware import GroupOnlyMiddleware

router = Router()
router.message.middleware(GroupOnlyMiddleware())


@router.message(Command('start_group'))
async def start_group(
    message: Message
):
    return await message.answer('okey')
