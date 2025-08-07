from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states import GroupReg
from keyboards import inl_games
from database import GroupsRepository
from schemas import GroupsBase


router = Router()


@router.message(GroupReg.group_name)
async def add_group_name(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    group_repo = GroupsRepository(
        session = session
    )

    if '@' in message.text:
        
        if await group_repo.get_by_name(
            name=message.text
        ):
           return await message.answer('Данная группа уже зарегестрирована')
            
        await state.update_data(
            group_name = message.text
        )

        await state.set_state(GroupReg.games)

        return await message.answer(
            'Выберы:',
            reply_markup=inl_games.games_list
            )
    
    return await message.answer('Вы ввели некорректные данные! Попробуйте снова.')


@router.callback_query(GroupReg.games)
async def add_group_games(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    
    await callback.answer()

    await state.update_data(
        games = callback.data
    )

    data = await state.get_data()

    group_repo = GroupsRepository(
        session = session
    )

    group_entity = GroupsBase(
        group_name=data["group_name"],
        games=data["games"]
    )

    new_group = await group_repo.create(
        user_id=callback.from_user.id,
        entity=group_entity
    )

    await state.clear()

    return await callback.message.answer(
        f"Вы настроили игру {new_group.games} для чата {new_group.group_name}"
    )