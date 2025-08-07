from pydantic import BaseModel

class UsersBase(BaseModel):
    telegram_id: int
    telegram_username: str
    creator: bool = False
    is_superuser: bool = False

