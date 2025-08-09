from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database import PartiesRepository, UsersRepository
from states import PartiesCreate


router = Router()


@router.callback_query(F.data.startswith("accept_party_"))
async def accept_party_handler(
    callback: CallbackQuery, 
    state: FSMContext,
    session: AsyncSession
):
    await callback.answer()
    party_info = callback.data.split("_")

    if party_info[4] != str(callback.from_user.id):
        return await callback.message.answer('Вы не можете учавствовать в данной партии')

    parties_repo = PartiesRepository(
        session=session
    )

    current_party = await parties_repo.read(
        id=int(party_info[2])
    )

    if current_party is None:
        return await callback.message.answer('Данная партия уже закончена')
    
    if current_party.status != 'waiting':
        return
    
    await state.set_state(PartiesCreate.creator_value)

    users_repo = UsersRepository(
        session=session
    )

    current_user = await users_repo.get_by_telegram_id(
        telegram_id=int(party_info[3])
    )

    return await callback.message.answer(f'первый ход делает {current_user.telegram_username}')



@router.message(PartiesCreate.creator_value)
async def set_creator_value(
    message: Message,
    state: FSMContext
):
    
    if not message.dice:
        return await message.answer("НУЖНО КИНУТЬ КУБ")
    
    await state.update_data(
        creator_value=int(message.dice.value)
    )

    await state.set_state(
        PartiesCreate.opponent_value
    )

    return await message.answer('ТЕПЕРЬ ХОДИТ ОППОНЕНТ')

    
@router.message(PartiesCreate.opponent_value)
async def set_opponent_value(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    
    if not message.dice:
        return await message.answer("НУЖНО КИНУТЬ КУБ")
    
    await state.update_data(
        opponent_value=int(message.dice.value)
    )

    data = await state.get_data()

    await state.clear()

    return await message.answer('Вы выйграли')