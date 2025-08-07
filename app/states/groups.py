from aiogram.fsm.state import State, StatesGroup


class GroupReg(StatesGroup):
    group_name: str = State()
    games: str = State()