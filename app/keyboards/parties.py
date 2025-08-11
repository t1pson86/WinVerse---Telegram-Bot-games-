from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardParties():

    def get_party_menu(self, party_id: int, creator_id: int, opponent_id: int):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Принять', callback_data=f"accept_party_{party_id}_{creator_id}_{opponent_id}")],
            [InlineKeyboardButton(text='❌ Отклонить', callback_data=f"decline_party_{party_id}_{creator_id}_{opponent_id}")],
            ])
        

inl_parties = InlineKeyboardParties()