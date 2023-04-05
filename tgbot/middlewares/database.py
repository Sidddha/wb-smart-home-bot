from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from tgbot.utils.db_api.user import User
from tgbot.utils.db_api.postgresql import Database

db = Database()


class GetDBUser(BaseMiddleware):
    """ 
    Перехватывает сообщение и возвращает данные пользователя из бд. 
    Если пользователь не обнаружен добавляет в юд с пометкой 'UNKNOWN_USER'
    """
    async def on_process_message(self, message: types.Message, data: dict):
        user = db.select_user(id=message.from_user.id)
        if user is None:
            db.add_user(message.from_user.id,
                        message.from_user.first_name, "UNKNOWN_USER")
            user = db.select_user(**{"id": message.from_user.id})           
        data["user"] = User(id=user[0], name=user[1], status=user[2])

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user = db.select_user(id=cq.from_user.id)
        if user is None:
            db.add_user(cq.from_user.id,
                        cq.from_user.full_name, "UNKNOWN_USER")
            user = db.select_user(**{"id": cq.from_user.id})
        data["user"] = User(id=user[0], name=user[1], status=user[2])
