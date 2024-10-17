from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit
from tgbot.keyboards.main_keyboard import main_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from loader import  bot
from tgbot.utils.db_api.db_commands import Database 
# from javascript import require

# dashboard = require("../../../wb-rules-modules/dashboard.js")

db = Database()
btn = Button()

@rate_limit(limit=1)
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}\n",
                        reply_markup=keyboard_constructor(btn.get_widgets, btn.devices))

async def retranslate(message: types.Message, user: User):
    print(f"Get message from {user.name}")
    for admin in db.get_admins():
        print(f"Resend to {admin.name}. text: {message.text}")
        message.forward(admin.id)

def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*", is_user=True)
    # dp.register_message_handler(callback=retranslate)


