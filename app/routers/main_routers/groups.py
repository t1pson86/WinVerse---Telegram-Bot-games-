from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database import UsersRepository
from schemas import UsersBase
from states import GroupReg

router = Router()


@router.callback_query(F.data == 'add_group')
async def add_group(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await callback.answer('add_group')

    user_entity = UsersBase(
        telegram_id=callback.from_user.id,
        telegram_username=callback.from_user.username
    )

    current_user = UsersRepository(
        session=session
    )

    res = await current_user.create(
        entity=user_entity
    )

    await state.set_state(GroupReg.group_name)

    return await callback.message.answer(
        'название чата:'
        )



