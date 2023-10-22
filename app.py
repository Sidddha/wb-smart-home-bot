import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.config import load_config

from tgbot import filters
from tgbot import handlers
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot import middlewares
from tgbot.utils.db_api import db_commands
from loader import config, bot, dp, logger
from tgbot.utils.db_api.db_commands import Database

logger = logging.getLogger(__name__)
db = Database()

async def set_commands(dp):
    await set_default_commands(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    middlewares.register_all_middlewares(dp)
    filters.register_all_filters(dp)
    handlers.register_handlers(dp)

    await set_commands(dp)
    
    try:
        db.create_table_users()
    except Exception as e:
        logger.exception(e)
    # db.add_user(504168024, "Siddha", "USER")
    # db.update_status(504168024, "ADMIN")
    print(db.get_all_users())
    await on_startup_notify(dp)

   # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
