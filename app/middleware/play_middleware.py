from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from dependencies import get_group_by_name

class GroupOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        
        if event.chat.type not in ("group", "supergroup"):
            return await event.answer("❌ Бот работает только в группах!")

        if not await get_group_by_name(name = event.chat.username):
            print(event.chat.username)
            return await event.answer("⚠️ Ваша группа не зарегистрирована! Обратитесь к администратору.")

        return await handler(event, data)