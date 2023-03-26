from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from tgbot.utils.db_api.user import User


class GetDBUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data["user"] = User(id=message.from_user.id,
                            name=message.from_user.full_name)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        data["user"] = User(id=cq.from_user.id, name=cq.from_user.full_name)
