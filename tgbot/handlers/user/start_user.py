from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit
from tgbot.keyboards.main_keyboard import main_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from loader import  bot
from tgbot.utils.db_api.db_commands import Database 
from javascript import require

dashboard = require("../../../wb-rules-modules/dashboard.js")

db = Database()
btn = Button()

@rate_limit(limit=1)
async def start(message: types.Message, user: User):
    await message.answer(f"Привет, {user.name}\n"
                        f"Здесь будет стандартное меню пользователя")
    await message.answer(f"Привет, {message.from_user.first_name}\n",
                        reply_markup=keyboard_constructor(btn.get_widgets, btn.devices, btn.settings, btn.system))

async def get_widgets(cq: types.CallbackQuery):
    """
    Handler for mangind devices placed in certain rooom.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - state (FSMContext): The FSM context.
    """

    # await cq.message.edit_text(f"Введи пароль доступа или отправь запрос администратору")
    # await cq.message.edit_reply_markup(keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    # await cq.message.delete_reply_markup()
    await cq.answer(text=str(dashboard.widgets), show_alert=True)
    # await state.reset_state(with_data=False)

async def retranslate(message: types.Message, user: User):
    print(f"Get message from {user.name}")
    for admin in db.get_admins():
        print(f"Resend to {admin.name}. text: {message.text}")
        message.forward(admin.id)

def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*", is_user=True)
    dp.register_callback_query_handler(get_widgets, main_callback.filter(command="get_widgets"), state="*")
    dp.register_message_handler(callback=retranslate)


