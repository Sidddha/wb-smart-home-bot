import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottledMiddleware(BaseMiddleware):
    """
    Middleware that limits the frequency of message sending for users.
    """

    def __init__(self, limit=0.5, key_prefix='antiflood_'):
        """
        Initialize the ThrottledMiddleware.

        Arguments:
        - limit (float): The rate limit in seconds.
        - key_prefix (str): The prefix for the throttling key.
        """
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottledMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Event handler for processing messages.

        Arguments:
        - message (types.Message): The message object.
        - data (dict): Additional data.

        Raises:
        - CancelHandler: If the message is throttled.

        Modifies:
        - data["user"]: User data retrieved from the database.
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t, limit)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled, limit):
        """
        Handler for throttled messages.

        Arguments:
        - message (types.Message): The throttled message object.
        - throttled (Throttled): The Throttled object.
        - limit (float): The rate limit in seconds.
        """
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await message.reply(f'Too frequent message sending. The limit is set to {limit} s.')
        await asyncio.sleep(delta)
