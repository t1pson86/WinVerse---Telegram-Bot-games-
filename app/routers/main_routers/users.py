from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database import UsersRepository
from schemas import UsersBase
from middleware import GroupOnlyMiddleware


router = Router()
router.message.middleware(GroupOnlyMiddleware())


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

    if not new_user:
        return await message.answer(f"""
<b>🎉 @{message.from_user.username}</b>

<b>Регистрация прошла успешно!</b>
Теперь вам доступны все возможности бота.
Можете создавать игры и участвовать в них!""",
parse_mode='HTML'
)
    return await message.answer(f"""
⚠️ @{message.from_user.username}

<b>Вы уже зарегестрированы!</b>
""",
    parse_mode='HTML'
)
