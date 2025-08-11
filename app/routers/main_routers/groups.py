from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from middleware import GroupOnlyMiddleware
from database import GroupsRepository, UsersRepository
from schemas import GroupsBase, UsersBase
from keyboards import inl_games

router = Router()
router.message.middleware(GroupOnlyMiddleware())


@router.message(Command('start_games'))
async def start_group(
    message: Message,
    bot: Bot,
    session: AsyncSession
) -> str:
    
    chat_admins = await bot.get_chat_administrators(message.chat.id)

    current_admin = [admin.user.id for admin in chat_admins if admin.status == 'creator'][0]

    if message.from_user.id != current_admin:
        return await message.answer("""
⛔ <b>Ограничение прав</b>
                                    
Активировать бота может только:
• Создатель группы
• Администратор с полными правами
                                    
Это необходимо для безопасности группы.
""",
    parse_mode='HTML'                                
    )

    user_repo = UsersRepository(
        session=session
    )

    user_entity = UsersBase(
        telegram_id=message.from_user.id,
        telegram_username='@' + message.from_user.username,
        creator=True
    )

    current_user = await user_repo.create(
        entity=user_entity
    )

    groups_repo = GroupsRepository(
        session=session
    )

    group_entity = GroupsBase(
        group_id=message.chat.id,
        group_name='@' + message.chat.username
    )

    new_group = await groups_repo.create(
        user_id=message.from_user.id,
        entity=group_entity
    )

    return await message.answer("""
🎮 <b>Игровой бот активирован!</b>
Теперь в этой группе можно играть в различные игры.
                                
Доступные игры:
🎲 Кости - /dice @username
                                
Выберите игру из меню ниже:
""",
    reply_markup=inl_games.games_list,
    parse_mode='HTML'
    )