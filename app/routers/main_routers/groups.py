from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from schemas import GroupsBase
from database import GroupsRepository

router = Router()


@router.message(Command('/app'))
async def app(
    message: Message,
    groups_repo: GroupsRepository,
    user_id: int = 1,
    games: str = 'dice'
):
    new_gr = GroupsBase(
        group_id=message.chat.id,
        group_name=message.chat.full_name,
        games=games
    )

    res = await groups_repo.create(
        user_id=user_id,
        entity=new_gr
    )

    return await message.answer('Okey')

