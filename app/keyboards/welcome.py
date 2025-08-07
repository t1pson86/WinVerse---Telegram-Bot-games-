from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardWelcome():

    def __init__(self):

        self.welcome = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🪙 Добавить группу', callback_data='add_group')]
            ])
        

inl_welcome = InlineKeyboardWelcome()