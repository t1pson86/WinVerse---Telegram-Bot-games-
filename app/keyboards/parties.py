from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardParties():

    def get_party_menu(self, party_id):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Принять', callback_data=f"accept_party_{party_id}")],
            [InlineKeyboardButton(text='Отклонить', callback_data=f"decline_party_{party_id}")],
            ])
        

inl_parties = InlineKeyboardParties()