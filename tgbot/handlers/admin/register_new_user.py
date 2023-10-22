from aiogram import Dispatcher, types
from tgbot.keyboards.registration_keyboard import registration_callback
from loader import  bot
from tgbot.utils.db_api.db_commands import Database 
import re

db = Database()

async def accept(cq: types.CallbackQuery):
    """
    Callback function to grant access to a new user. Called by an administrator.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    """

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    id = int(id[0])
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    db.update_status(id=id)
    await cq.answer(text=f"Пользователь {name[0]} добавлен!", show_alert=True)
    await cq.message.delete_reply_markup()
    await bot.send_message(chat_id=id, text="Доступ разрешен. Чтобы начать работу введите команду /start")

async def make_admin(cq: types.CallbackQuery):
    """
    Callback function to grant access with administrator rights to a new user. Called by an administrator.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    """

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    id = int(id[0])
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    db.update_status(id=id, status="ADMIN")
    await cq.answer(text=f"Пользователь {name[0]} добавлен как администратор!", show_alert=True)
    await cq.message.delete_reply_markup()
    await bot.send_message(chat_id=id, text="Доступ разрешен с правами администратора. Чтобы начать работу введите команду /start")

async def refuse(cq: types.CallbackQuery):
    """
    Callback function to deny access. Called by an administrator.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    """

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    id = int(id[0])
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    await bot.send_message(chat_id=id, text="Вам отказано в доступе. Увы")
    await cq.answer(text=f"Пользователю {name[0]} отказано в доступе", show_alert=True)
    await cq.message.delete_reply_markup()


def register_new_user(dp: Dispatcher):
    """
    Function to register new user callbacks with the dispatcher.

    Arguments:
    - dp (Dispatcher): The dispatcher object.
    """

    dp.register_callback_query_handler(accept, registration_callback.filter(reg="accept"), state="*")
    dp.register_callback_query_handler(refuse, registration_callback.filter(reg="refuse"), state="*")
    dp.register_callback_query_handler(make_admin, registration_callback.filter(reg="make_admin"), state="*")