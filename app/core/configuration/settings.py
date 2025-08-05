import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class BotSettings(BaseSettings):

    bot_token: str = os.getenv("BOT_TOKEN")

bot_settings = BotSettings()


class DatabaseSettings(BaseSettings):
    
    url_database: str = f'sqlite+aiosqlite:///{os.getenv("DB_NAME")}'

db_settings = DatabaseSettings()
