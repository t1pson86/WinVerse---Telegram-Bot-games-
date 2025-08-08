from aiogram.fsm.state import State, StatesGroup

class PartiesCreate(StatesGroup):
    creator_value: int = State()
    opponent_value: int = State()
    