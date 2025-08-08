from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class GroupOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        
        if event.chat.type not in ("group", "supergroup"):
            return await event.answer("❌ Данная команда работает только в группах!")

        return await handler(event, data)