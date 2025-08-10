from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message

from database import PartiesRepository, UsersRepository


router = Router()


@router.callback_query(F.data.startswith("accept_party_"))
async def accept_party_handler(
    callback: CallbackQuery, 
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
    
    if current_party.status == 'accept':
        return await callback.message.answer('Данная партия уже идет или была завершена.')
    
    update_status_party = await parties_repo.update(
        party_id=int(party_info[2]),
        new_status='accept'
    )

    users_repo = UsersRepository(
        session=session
    )

    current_user = await users_repo.get_by_telegram_id(
        telegram_id=int(party_info[3])
    )

    return await callback.message.answer(f"""
✅ <b>Игра принята!</b>
                                         
🎲 Игра в кости началась между:
👤 {current_user.telegram_username}
👤 @{callback.from_user.username}

Кидайте кубик (отправьте emoji 🎲)!
Кто выбросит большее число - победит!""",

    parse_mode='HTML'
    )



@router.message(F.dice)
async def set_value(
    message: Message,
    session: AsyncSession
):
    parties_repo = PartiesRepository(
        session=session
    )

    current_party_by_creator = await parties_repo.get_party_by_creator_id(
        creator_id=message.from_user.id
    )

    user_repo = UsersRepository(
        session=session
    )

    dice_data = message.dice.value

    if current_party_by_creator is None:
        
        current_party_by_opponent = await parties_repo.get_party_by_opponent_id(
            opponent_id=message.from_user.id
        )

        if current_party_by_opponent is None:
            return
       
        if current_party_by_opponent.opponent_value:
            return

        update_opponent_data = await parties_repo.update_party_info_by_opponent_id(
            opponent_id=message.from_user.id,
            new_value=dice_data
        )

        info_opponent = await user_repo.get_by_telegram_id(
            telegram_id=current_party_by_opponent.opponent_id
        )

        creator_name = await user_repo.get_by_telegram_id(
            telegram_id=current_party_by_opponent.creator_id
        )
        
        if current_party_by_opponent.creator_value:
            del_party = await parties_repo.delete(
                id=current_party_by_opponent.id
            )
            if dice_data == current_party_by_opponent.creator_value:
                return await message.answer(f"""
🤝 <b>Ничья!</b>
                                    
Оба игрока выбросили {dice_data} очков.
Попробуйте сыграть ещё раз!""",
parse_mode='HTML'
    )
            if dice_data > current_party_by_opponent.creator_value:
                return await message.answer(f"Победил {info_opponent.telegram_username}")
            if dice_data < current_party_by_opponent.creator_value:
                return await message.answer(f"Победил {creator_name.telegram_username}")
        
        creator_username_info = await user_repo.get_by_telegram_id(
            telegram_id=current_party_by_opponent.creator_id
        )

        return await message.answer(
            f"""
<b>⏳ Ожидаем ход от {creator_username_info.telegram_username}.</b>

Вы выбросили <b>{dice_data}</b> очков.
            """,
            parse_mode='HTML'
        )

    if current_party_by_creator.creator_value:
        return

    if current_party_by_creator.status == 'waiting':
        return

    update_creator_data = await parties_repo.update_party_info_by_creator_id(
        creator_id=message.from_user.id,
        new_value=dice_data
    )


    info_creator = await user_repo.get_by_telegram_id(
        telegram_id=current_party_by_creator.creator_id
    )

    opponent_name = await user_repo.get_by_telegram_id(
        telegram_id=current_party_by_creator.opponent_id
    )

    if current_party_by_creator.opponent_value:
        del_party = await parties_repo.delete(
            id=current_party_by_creator.id
        )
        if dice_data == current_party_by_creator.opponent_value:
            return await message.answer(f"""
🤝 <b>Ничья!</b>
                                    
Оба игрока выбросили {dice_data} очков.
Попробуйте сыграть ещё раз!""",
parse_mode='HTML'
    )
        if dice_data > current_party_by_creator.opponent_value:
            return await message.answer(f"Победил {info_creator.telegram_username}")
        if dice_data < current_party_by_creator.opponent_value:
            return await message.answer(f"Победил {opponent_name.telegram_username}")
    
    return await message.answer(
            f"""
<b>⏳ Ожидаем ход от {info_creator.telegram_username}.</b>

Вы выбросили <b>{dice_data}</b> очков.
            """,
            parse_mode='HTML'
        )
    