from .db import db_conn

async def get_new_async_session():
    async with db_conn.async_session() as session:
        yield session

