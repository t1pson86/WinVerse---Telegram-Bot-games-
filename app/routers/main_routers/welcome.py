from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from middleware import ChatOnlyMiddleware


router = Router()
router.message.middleware(ChatOnlyMiddleware())


@router.message(CommandStart())
async def start(
    message: Message
):

    return await message.answer("""
<b>👋 Добро пожаловать в @WinVerseBot!</b>
                        
Чтобы начать использовать бота в группе:
1. Добавьте бота в свой чат/группу
2. Назначьте бота администратором
3. Администратор группы должен ввести команду /start_games
4. После этого можно начинать играть!""",
    
    parse_mode='HTML'
    
    )