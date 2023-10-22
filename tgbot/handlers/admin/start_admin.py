from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc.throttling import rate_limit

@rate_limit(limit=1)
async def admin_start(message: Message):
    """
    Handler for the admin start command.

    Arguments:
    - message (Message): The message object.
    """

    await message.answer(f"Привет, {message.from_user.first_name}\n"
                        "Здесь будет расширенное меню администратора")


def register_admin(dp: Dispatcher):
    """
    Function to register the admin start command handler with the dispatcher.

    Arguments:
    - dp (Dispatcher): The dispatcher object.
    """

    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)