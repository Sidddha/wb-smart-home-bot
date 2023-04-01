import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, remove_admin
from tgbot import filters
from tgbot import handlers
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot import middlewares
from tgbot.utils.db_api.sqlite import Database


logger = logging.getLogger(__name__)

db = Database()
config = load_config(".env")
storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    middlewares.setup(dp)


async def set_commands(dp):
    await set_default_commands(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot['config'] = config

    register_all_middlewares(dp, config)
    filters.register_all_filters(dp)
    handlers.register_handlers(dp)
    await set_commands(dp)
    await on_startup_notify(dp)
    # db.delete_users()
    # remove_admin(504168024)
    try:
        db.create_table_users()
    except Exception as e:
        logger.exception(e)
    # db.add_user(504168024, "Siddha", "USER")
    # db.update_status("ADMIN", 504168024)
    print(db.select_all_users())

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
