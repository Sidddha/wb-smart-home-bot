from aiogram import Dispatcher, types
from tgbot.keyboards.registration_keyboard import registration_callback
from loader import  bot
from tgbot.utils.db_api import quick_commands as db
import re


async def accept(cq: types.CallbackQuery):
    """Колбэк функция для разрешения доступа новому пользователю. Вызывается администратором"""

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    await db.update_status(id=id[0])
    await cq.answer(text=f"Пользователь {name[0]} добавлен!", show_alert=True)
    await bot.send_message(chat_id=id[0], text="Доступ разрешен. Чтобы начать работу введите команду /start")

async def make_admin(cq: types.CallbackQuery):
    """Колбэк функция для разрешения доступа с правами администратора новому пользователю. Вызывается администратором"""

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    await db.update_status(id=id[0], status="ADMIN")
    await cq.answer(text=f"Пользователь {name[0]} добавлен как администратор!", show_alert=True)
    await bot.send_message(chat_id=id[0], text="Доступ разрешен с правами администратора. Чтобы начать работу введите команду /start")
   

async def refuse(cq: types.CallbackQuery):
    """Колбэк функция для запрещения доступа. Вызывается администратором"""

    id = re.findall(r'(?<=ID=)\d+', cq.message.text)
    name = re.findall(r'Пользователь\s+(\w+)', cq.message.text)
    await bot.send_message(chat_id=id[0], text="Вам отказано в доступе. Увы")
    await cq.answer(text=f"Пользователю {name[0]} отказано в доступе", show_alert=True)


def register_new_user(dp: Dispatcher):
    dp.register_callback_query_handler(accept, registration_callback.filter(reg="accept"), state="*")
    dp.register_callback_query_handler(refuse, registration_callback.filter(reg="refuse"), state="*")
    dp.register_callback_query_handler(make_admin, registration_callback.filter(reg="make_admin"), state="*")