from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from tgbot.utils.db_api.user import User
from tgbot.utils.db_api.sqlite import Database

db = Database()

class GetDBUser(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        user = User(id=message.from_user.id, name=message.from_user.full_name)
        data["user"] = db.select_user(user.id)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user = User(id=cq.from_user.id, name=cq.from_user.full_name)
        data["user"] = db.select_user(user.id)
