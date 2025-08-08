from pydantic import BaseModel

class PartiesBase(BaseModel):
    game_type: str
    creator_id: int
    opponent_id: int
    creator_value: int
    opponent_value: int