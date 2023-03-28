from .calback_datas import registration_callback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Ввести пароль", callback_data=registration_callback.new(choice="enter_password"))
    ],
    [
        InlineKeyboardButton(
            text="Отправить запрос", callback_data=registration_callback.new(choice="send_request"))
    ],
    [
        InlineKeyboardButton(
            text="Отмена", callback_data=registration_callback.new(choice="cancel"))
    ]
])
