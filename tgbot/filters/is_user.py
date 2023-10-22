from aiogram.dispatcher.filters import BoundFilter

import typing

from tgbot.utils.db_api.db_commands import Database

db = Database()

class UserFilter(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, obj):
        try:
            user = db.get_user(id=obj.from_user.id)
            if user.status is None:
                return False
            else:
                print(f"========== status = {user.status}")
                if user.status == "USER":
                    return self.is_user
        except AttributeError:
            pass