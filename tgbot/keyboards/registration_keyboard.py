from .calback_datas import registration_callback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from button_constructor import Button

class Button():
    def __init__(self):
        self.text = ""
        self.callback_data = ""
        self.enter_password = {
            "text": "Ввести пароль",
            "callback_data": registration_callback.new(reg="enter_password")
        }
        self.send_request= {
            "text": "Отправить запрос", 
            "callback_data": registration_callback.new(reg="send_request")
        }
        self.accept= {
            "text": "Принять", 
            "callback_data": registration_callback.new(reg="accept")           
        }
        self.refuse= {
            "text": "Отклонить", 
            "callback_data": registration_callback.new(reg="refuse")           
        }   
        self.make_admin= {
            "text": "Назначить администратором",
            "callback_data": registration_callback.new(reg="make_admin")
        }            
        self.cancel= {
            "text": "Отмена", 
            "callback_data": registration_callback.new(reg="cancel")
        }
        self.debug= {
            "text": "DEBUG_MODE: reset attempts",
            "callback_data": registration_callback.new(reg="debug")
        }


# def registration_keyboard(*buttons):
#     keyboard = InlineKeyboardMarkup()
#     for button in buttons:
#         text = button["text"]
#         callback_data = button["callback_data"]
#         keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))
#     return keyboard



