from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit


@rate_limit(limit=10)
async def start(message: types.Message, user: User):
    await message.answer(f"Hello, {user.name}\n"
                         f"User got via middleware: {user.__dict__}")


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")


