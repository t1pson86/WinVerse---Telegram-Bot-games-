from aiogram import BaseMiddleware

from database import db_conn


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with db_conn.async_session() as session:
            data["session"] = session
            return await handler(event, data)