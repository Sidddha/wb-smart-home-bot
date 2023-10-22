from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from tgbot.utils.db_api.user import User
from tgbot.utils.db_api.db_commands import Database

db = Database()

class GetDBUser(BaseMiddleware):
    """
    Middleware that intercepts a message and retrieves user data from the database.
    If the user is not found, it adds the user to the database with the status 'UNKNOWN_USER'.
    """

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Event handler for processing messages.

        Arguments:
        - message (types.Message): The message object.
        - data (dict): Additional data.

        Modifies:
        - data["user"]: User data retrieved from the database.
        """
        user = db.get_user(id=message.from_user.id)
        if user is None:
            print("--------------------------")
            print(message.chat)
            db.add_user(id=message.from_user.id, chat=message.chat.id, name=message.from_user.first_name, status="UNKNOWN_USER")
            user = db.get_user(id=message.from_user.id)
        data["user"] = User(id=user.id, chat=user.chat, name=user.name, status=user.status)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        """
        Event handler for processing callback queries.

        Arguments:
        - cq (types.CallbackQuery): The callback query object.
        - data (dict): Additional data.

        Modifies:
        - data["user"]: User data retrieved from the database.
        """
        user = db.get_user(id=cq.from_user.id)
        if user is None:
            db.add_user(id=cq.from_user.id, chat=cq.message.chat.id, name=cq.from_user.full_name, status="UNKNOWN_USER")
            user = db.get_user(id=cq.from_user.id)
        data["user"] = User(id=user.id, chat=user.chat, name=user.name, status=user.status)