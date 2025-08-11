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
    return await callback.answer(text="""
🎲 Как начать игру:
                                 
Используйте:    /dice @username
                                 
Где @username — это ник игрока
которого хотите вызвать на дуэль!
""",
    show_alert=True
)



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
Администратор должен сначала ввести команду /start_games
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
        return await message.answer(f"""
<b>⚠️ @{message.from_user.username}</b>

Вы не можете предложить игру самому себе.""",
parse_mode='HTML'
)
    
    user_repo = UsersRepository(
        session=session
    )

    if not await user_repo.get_by_name(name='@'+message.from_user.username):
        return await message.answer(f"""
<b>🔒 {'@'+message.from_user.username}</b>
Вы не зарегистрированы!
Введите команду <b>/reg</b> для доступа к играм.""",
parse_mode='HTML'
        )

    opponent_info_id = await user_repo.get_by_name(name=opponent_telegram_info[1])

    if not opponent_info_id:
        return await message.answer(f"""
<b>👤 Пользователь {opponent_telegram_info[1]} не зарегистрирован!</b>
Попросите его ввести <b>/reg</b>.""",
parse_mode='HTML'
    )

    parties_repo = PartiesRepository(
        session=session
    )

    current_creator_party = await parties_repo.get_party_by_creator_id(
        creator_id=message.from_user.id
    )

    current_opponent_party = await parties_repo.get_party_by_opponent_id(
        opponent_id=message.from_user.id
    )

    if current_creator_party:
        return await message.answer(f"""
⚠️ <b>У вас есть активная партия!</b>
                                    
🎲 Вы не можете создать новую игру, пока не завершите текущую.
Если соперник не отвечает:
1. Нажмите кнопку <b>❌ ОТКЛОНИТЬ</b> под игровым сообщением
2. Или подождите еще немного
                                    
<i>После завершения партии вы сможете начать новую</i>,
""",
parse_mode='HTML'
)

    if current_opponent_party:
        return await message.answer(f"""
⚠️ <b>У вас есть активная партия!</b>
                                    
🎲 Вы не можете создать новую игру, пока не завершите текущую.
Если соперник не отвечает:
1. Нажмите кнопку <b>❌ ОТКЛОНИТЬ</b> под игровым сообщением
2. Или подождите еще немного
                                    
<i>После завершения партии вы сможете начать новую</i>,
""",
parse_mode='HTML'
)
    
    check_creator_info = await parties_repo.get_party_by_creator_id(
        creator_id=opponent_info_id.telegram_id
    )
    if check_creator_info:
        return await message.answer(f"""
🎲 <b>Кто-то опередил вас!</b>
                                    
{opponent_telegram_info[1]} уже в игре

⏳ Пожалуйста, подождите или выберите другого соперника
<i>Попробуйте снова через пару минут!</i>
""",
    parse_mode='HTML'
)
    check_opponent_info = await parties_repo.get_party_by_opponent_id(
        opponent_id=opponent_info_id.telegram_id
    )

    if check_opponent_info:
        return await message.answer(f"""
🎲 <b>Кто-то опередил вас!</b>
                                    
{opponent_telegram_info[1]} уже в игре

⏳ Пожалуйста, подождите или выберите другого соперника
<i>Попробуйте снова через пару минут!</i>
""",
    parse_mode='HTML'
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
                                           
👤 <b>Игрок 1</b>: @{message.from_user.username}
👤 <b>Игрок 2</b>: {opponent_telegram_info[1]}

{opponent_telegram_info[1]} должен принять или отклонить вызов ниже 👇""",

    reply_markup=inl_parties.get_party_menu(
        party_id=current_party.id,
        creator_id=message.from_user.id,
        opponent_id=opponent_info_id.telegram_id
        ),

        parse_mode='HTML'
        )