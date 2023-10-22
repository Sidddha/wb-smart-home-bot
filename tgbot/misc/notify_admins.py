import logging

from aiogram import Dispatcher
from tgbot.utils.db_api.db_commands import Database

db = Database()

async def on_startup_notify(dp: Dispatcher):
        admins = db.get_admins()
        print(admins)
        if admins:
            for admin in admins:
                try:
                    await dp.bot.send_message(admin.chat, "Бот запущен и готов к работе")
                except Exception as err:
                    logging.exception(err)

