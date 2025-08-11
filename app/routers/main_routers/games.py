import asyncio
from aiogram import Router, F, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message

from database import PartiesRepository, UsersRepository
from middleware import GroupOnlyMiddleware

router = Router()
router.message.middleware(GroupOnlyMiddleware())


@router.callback_query(F.data.startswith("accept_party_"))
async def accept_party_handler(
    callback: CallbackQuery, 
    bot: Bot,
    session: AsyncSession
):
    await callback.answer()
    party_info = callback.data.split("_")

    if party_info[4] != str(callback.from_user.id):
        return await callback.message.answer(f"""
❌ @{callback.from_user.username}

<b>Вы не можете принять данную партию.</b>
""",
    parse_mode='HTML'
    )

    parties_repo = PartiesRepository(
        session=session
    )

    current_party = await parties_repo.read(
        id=int(party_info[2])
    )

    if current_party is None:
        return await callback.message.answer("""
<b>❌ Данная партия уже завершилась.</b>
Больше нельзя принять участие!
""",
    parse_mode='HTML'
    )
    
    if current_party.status == 'accept':
        return await callback.message.answer("""
<b>⚠️ Партия уже идет.</b>
Принять нельзя!
""",
    parse_mode='HTML'
        )
    
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

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    return await callback.message.answer(f"""
✅ <b>Игра принята!</b>
                                         
🎲 Игра в кости началась между:
👤 <b>Игрок 1</b>: {current_user.telegram_username}
👤 <b>Игрок 2</b>: @{callback.from_user.username}

Кидайте кубик (отправьте 🎲)!
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
        
        if current_party_by_opponent.status == 'waiting':
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
            await asyncio.sleep(2.5)
            if dice_data == current_party_by_opponent.creator_value:
                return await message.answer(f"""
🤝 <b>Ничья!</b>
                                    
Оба игрока выбросили {dice_data} очков.
Попробуйте сыграть ещё раз!""",
parse_mode='HTML'
    )
            if dice_data > current_party_by_opponent.creator_value:
                return await message.answer(f"""
🏆 <b>Победитель: {info_opponent.telegram_username}!</b>

Результаты:
{info_opponent.telegram_username}: <b>{current_party_by_opponent.opponent_value} очков</b>
{creator_name.telegram_username}: <b>{current_party_by_opponent.creator_value} очков</b>

Поздравляем победителя! 🎉""",
parse_mode='HTML')
            
            if dice_data < current_party_by_opponent.creator_value:
                return await message.answer(f"""
🏆 <b>Победитель: {creator_name.telegram_username}!</b>

Результаты:
{creator_name.telegram_username}: <b>{current_party_by_opponent.creator_value} очков</b>
{info_opponent.telegram_username}: <b>{current_party_by_opponent.opponent_value} очков</b>

Поздравляем победителя! 🎉""",
parse_mode='HTML')
        
        creator_username_info = await user_repo.get_by_telegram_id(
            telegram_id=current_party_by_opponent.creator_id
        )

        await asyncio.sleep(2.5)

        return await message.answer(
            f"""
<b>⏳ Ожидаем ход от {creator_username_info.telegram_username}.</b>

Вы выбросили <b>{dice_data} очков</b>.
            """,
            parse_mode='HTML'
        )

    if current_party_by_creator.creator_value:
        return

    if current_party_by_creator.status == 'waiting':
        return
    
    info_creator = await user_repo.get_by_telegram_id(
        telegram_id=current_party_by_creator.creator_id
    )

    opponent_name = await user_repo.get_by_telegram_id(
        telegram_id=current_party_by_creator.opponent_id
    )

    update_creator_data = await parties_repo.update_party_info_by_creator_id(
        creator_id=message.from_user.id,
        new_value=dice_data
    )

    if current_party_by_creator.opponent_value:
        del_party = await parties_repo.delete(
            id=current_party_by_creator.id
        )
        await asyncio.sleep(2.5)
        if dice_data == current_party_by_creator.opponent_value:
            return await message.answer(f"""
🤝 <b>Ничья!</b>
                                    
Оба игрока выбросили <b>{dice_data} очков</b>.
Попробуйте сыграть ещё раз!""",
parse_mode='HTML'
    )
        if dice_data > current_party_by_creator.opponent_value:
            return await message.answer(f"""
🏆 <b>Победитель: {info_creator.telegram_username}!</b>

Результаты:
{info_creator.telegram_username}: <b>{current_party_by_creator.creator_value} очков</b>
{opponent_name.telegram_username}: <b>{current_party_by_creator.opponent_value} очков</b>

Поздравляем победителя! 🎉""",
parse_mode='HTML')
        if dice_data < current_party_by_creator.opponent_value:
            return await message.answer(f"""
🏆 <b>Победитель: {opponent_name.telegram_username}!</b>

Результаты:
{opponent_name.telegram_username}: <b>{current_party_by_creator.opponent_value} очков</b>
{info_creator.telegram_username}: <b>{current_party_by_creator.creator_value} очков</b>

Поздравляем победителя! 🎉""",
parse_mode='HTML')
        
    await asyncio.sleep(2.5)
    
    return await message.answer(
            f"""
<b>⏳ Ожидаем ход от {opponent_name.telegram_username}.</b>

Вы выбросили <b>{dice_data} очков</b>.
            """,
            parse_mode='HTML'
        )
    



@router.callback_query(F.data.startswith("decline_party_"))
async def decline_party_handler(
    callback: CallbackQuery,
    bot: Bot,
    session: AsyncSession
):
    await callback.answer()

    party_info = callback.data.split("_")
    
    parties_repo = PartiesRepository(
        session=session
    )

    current_party = await parties_repo.read(
        id=int(party_info[2])
    )

    if current_party.creator_id != callback.from_user.id and current_party.opponent_id != callback.from_user.id:
        return await callback.message.answer('⚠️ Отклонить данную партию могут только её игроки!')

    if current_party is None:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        return
    
    if current_party.status == 'accept':
        return await callback.message.answer("""
⚠️ <b>Данная партия уже идет.</b>
Нельзя отклонить!
""",
    parse_mode='HTML'
)
    
    user_repo = UsersRepository(
        session=session
    )

    user_data = await user_repo.get_by_telegram_id(
        telegram_id=int(party_info[3])
    )

    if user_data is None:
        return
    
    del_party = await parties_repo.delete(
        id=current_party.id
    )

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    return await callback.message.answer(f"""
⚡ <b>Игра отменена</b>
                                         
🙅‍♂️ Пользователь @{callback.from_user.username}
отклонил предложение сыграть в кости
🎲 От: {user_data.telegram_username}

<i>Может быть в следующий раз!</i>
""",
    parse_mode='HTML'
)