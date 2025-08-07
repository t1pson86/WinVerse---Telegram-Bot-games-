from pydantic import BaseModel


class GroupsBase(BaseModel):
    group_id: int = None
    group_name: str
    games: str