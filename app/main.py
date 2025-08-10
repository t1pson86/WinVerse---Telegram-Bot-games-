import asyncio
from aiogram import Bot, Dispatcher

from core import bot_settings
from routers import router
from database import db_conn, Base
from middleware import DbSessionMiddleware


bot = Bot(bot_settings.bot_token)

dp = Dispatcher()
dp.update.middleware(DbSessionMiddleware())


async def create_db():
    async with db_conn.engin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_db()
    dp.include_router(router=router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print('Close bot')
