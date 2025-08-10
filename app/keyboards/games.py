from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardGames():

    def __init__(self):

        self.games_list = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🎲 Кубы', callback_data='dice_game')],
            ])
        

inl_games = InlineKeyboardGames()