from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    q1 = State()
    q2 = State()

class NewUser(StatesGroup):
    password = State()
    request = State()
    attempts_limit = State()
