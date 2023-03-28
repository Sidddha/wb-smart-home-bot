from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.db_api.sqlite import Database
import typing

db = Database()

class UserFilter(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, obj):
        users = db.select_all_ids()
        for item in users:
            if item[0] == obj.from_user.id:
                if db.select_status(id=item[0]) == "USER":
                    return self.is_user
