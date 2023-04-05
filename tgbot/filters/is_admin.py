import typing

from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.db_api.postgresql import Database 
from tgbot.config import Config


db = Database()

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        # config: Config = obj.bot.get('config')
        # return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
        status = db.select_status(id=obj.from_user.id)
        if status is None:
            return False
        else:
            print(f"========== status = {status[0]}")
            if status[0] == "ADMIN":
                return self.is_admin
