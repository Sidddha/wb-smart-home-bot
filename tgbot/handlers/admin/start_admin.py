from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from tgbot.misc.throttling import rate_limit
from tgbot.keyboards.main_keyboard import main_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from loader import  bot, config
from tgbot.utils.db_api.db_commands import Database 
import re
from javascript import require
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.keyboards.callback_datas import widgets_callback, cells_callback
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import MainMenu

db = Database()
btn = Button()

@rate_limit(limit=1)
async def admin_start(message: Message):
    """
    Handler for the admin start command.

    Arguments:
    - message (Message): The message object.
    """

    await message.answer(f"Привет, {message.from_user.first_name}\n",
                        reply_markup=keyboard_constructor(btn.get_widgets, btn.devices, btn.settings, btn.system))
 
    
    
def register_admin(dp: Dispatcher):
    """
    Function to register the admin start command handler with the dispatcher.

    Arguments:
    - dp (Dispatcher): The dispatcher object.
    """

    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
