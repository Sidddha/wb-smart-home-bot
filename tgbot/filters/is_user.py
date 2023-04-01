from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.db_api.sqlite import Database
import typing
# from app import logger

db = Database()

class UserFilter(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, obj):
        status = db.select_status(id=obj.from_user.id)
        if status is None:
            return False
        else:
            print(f"========== status = {status[0]}")
            if status[0] == "USER":
                return self.is_user
