from aiogram import Dispatcher

from .throttling import ThrottledMiddleware
from .database import GetDBUser


def register_all_middlewares(dp: Dispatcher):
    dp.middleware.setup(ThrottledMiddleware())
    dp.middleware.setup(GetDBUser())
