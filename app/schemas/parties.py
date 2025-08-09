from pydantic import BaseModel

class PartiesBase(BaseModel):
    game_type: str
    status: str = 'waiting'
    creator_id: int
    opponent_id: int = None
    creator_value: int = None
    opponent_value: int = None