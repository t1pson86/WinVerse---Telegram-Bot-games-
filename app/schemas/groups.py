from pydantic import BaseModel


class GroupsBase(BaseModel):
    group_id: int
    group_name: str
    games: str