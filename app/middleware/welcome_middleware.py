from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class ChatOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        
        if event.chat.type in ("group", "supergroup"):
            return await event.answer("❌ Данная команда работает только в личном чате с ботом! @WinVerseBot")

        return await handler(event, data)