from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from core import db_settings

class DatabaseConnect():

    def __init__(self):
        self.engin = create_async_engine(
            url = db_settings.url_database
        )
        self.async_session = async_sessionmaker(
            bind = self.engin,
            class_ = AsyncSession,
            expire_on_commit = False
        )

db_conn = DatabaseConnect()


