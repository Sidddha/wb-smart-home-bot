import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
# from tgbot.handlers.testing import register_test
# from tgbot.handlers.admin import register_admin
# from tgbot.handlers.echo import register_echo
# from tgbot.handlers._user import register_user
from tgbot import handlers
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot import middlewares
from tgbot.utils.db_api.sqlite import Database


logger = logging.getLogger(__name__)

db = Database()

def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    middlewares.setup(dp)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


# def register_all_handlers(dp):
#     handlers.register_handlers(dp)
#     register_test(dp)
#     register_admin(dp)
#     register_user(dp)

#     register_echo(dp)


async def set_commands(dp):
    await set_default_commands(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    handlers.register_handlers(dp)
    await set_commands(dp)
    await on_startup_notify(dp)
    try:
        db.create_table_users()
    except Exception as e:
        logger.exception(e)
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
