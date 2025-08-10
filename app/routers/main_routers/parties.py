from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from middleware import GroupOnlyMiddleware
from database import UsersRepository, GroupsRepository, PartiesRepository
from keyboards import inl_parties
from schemas import PartiesBase


router = Router()
router.message.middleware(GroupOnlyMiddleware())


@router.callback_query(F.data == 'dice_game')
async def dice_game(
    callback: CallbackQuery
):
    return await callback.answer('Нужно прописать команду /dice username', show_alert=True)



@router.message(Command('dice'))
async def create_dice_party(
    message: Message,
    session: AsyncSession
):
    
    group_repo = GroupsRepository(
        session=session
    )

    current_group = await group_repo.read(
        id = message.chat.id
    )

    if current_group is None:
        return await message.answer(
        """
<b>⚠️ Группа не активирована!</b>
Администратор должен сначала ввести команду /start_game
        """,
        
        parse_mode='HTML'
        )

    opponent_telegram_info = message.text.split()

    if len(opponent_telegram_info) != 2 or '@' not in message.text:
        return await message.answer("""
<b>❌ Неправильный формат команды!</b>
Используйте: /dice @username
Пример: /dice @user123""",

    parse_mode='HTML'
    )
    
    if opponent_telegram_info[1] == '@'+message.from_user.username:
        return await message.answer('Вы не можете предложить игру самому себе.')
    
    user_repo = UsersRepository(
        session=session
    )

    if not await user_repo.get_by_name(name='@'+message.from_user.username):
        return await message.answer(f"""
🔒 {'@'+message.from_user.username} Вы не зарегистрированы!
Введите команду /reg для доступа к играм."""
        )

    opponent_info_id = await user_repo.get_by_name(name=opponent_telegram_info[1])

    if not opponent_info_id:
        return await message.answer(f"""
👤 Пользователь {opponent_telegram_info[1]} не зарегистрирован!
Попросите его ввести команду /reg."""
        )

    parties_repo = PartiesRepository(
        session=session
    )

    partie_entity = PartiesBase(
        game_type=opponent_telegram_info[1][1:],
        creator_id=message.from_user.id,
        opponent_id=opponent_info_id.telegram_id
    )

    current_party = await parties_repo.create(
        entity=partie_entity
    )

    return await message.answer(f"""
🎲 <b>Новая игра в кости!</b>  
                                           
👤 Игрок 1: @{message.from_user.username}
👤 Игрок 2: {opponent_telegram_info[1]}

{opponent_telegram_info[1]} должен принять вызов ниже 👇""",

    reply_markup=inl_parties.get_party_menu(
        party_id=current_party.id,
        creator_id=message.from_user.id,
        opponent_id=opponent_info_id.telegram_id
        ),

        parse_mode='HTML'
        )