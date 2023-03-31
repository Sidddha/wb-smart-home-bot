import typing

from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.db_api.sqlite import Database 
from tgbot.config import Config


db = Database()

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        # if self.is_admin is None:
        #     return False
        # config: Config = obj.bot.get('config')
        # return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
        users = db.select_all_ids()
        print(f"================= {users}")
        for item in users:
            if item[0] == obj.from_user.id:
                if db.select_status(id=item[0]) == "ADMIN":
                    return self.is_admin

