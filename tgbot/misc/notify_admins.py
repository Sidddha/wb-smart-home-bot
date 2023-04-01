import logging

from aiogram import Dispatcher
from tgbot.config import load_config

async def on_startup_notify(dp: Dispatcher):
    config = load_config()
    for admin in config.tg_bot.admin_ids:
        try:
            await dp.bot.send_message(admin, "Бот запущен и готов к работе")
        except Exception as err:
            logging.exception(err)