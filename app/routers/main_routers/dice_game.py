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


@router.callback_query(F.data == 'dice_game_1')
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
        return await message.answer('Чтобы пользоваться ботом администратор должен прописать /start_game')

    opponent_telegram_info = message.text.split()

    if len(opponent_telegram_info) != 2 or '@' not in message.text:
        return await message.answer('Неправильный формат')
    
    user_repo = UsersRepository(
        session=session
    )

    if not await user_repo.get_by_name(name='@'+message.from_user.username):
        return await message.answer('Введите команду /reg, чтобы можно было создать игру')

    if not await user_repo.get_by_name(name=opponent_telegram_info[1]):
        return await message.answer(f'Пользователь {opponent_telegram_info[1]} Введите команду /reg, чтобы можно было создать игру')

    parties_repo = PartiesRepository(
        session=session
    )

    partie_entity = PartiesBase(
        game_type=
    )

    current_party = await parties_repo.create(
        entity=
    )

    return await message.answer(
        f'Пользователь @{message.from_user.username} предложил игру пользователю {opponent_telegram_info[1]}',
        reply_markup=inl_parties.get_party_menu(
            party_id=
        )
        )