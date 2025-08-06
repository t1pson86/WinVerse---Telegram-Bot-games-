from pydantic import BaseModel

class UsersBase(BaseModel):
    telegram_id: int
    telegram_username: str
    is_superuser: bool = False

