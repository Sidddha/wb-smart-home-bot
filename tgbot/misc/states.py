from aiogram.dispatcher.filters.state import StatesGroup, State

class NewUser(StatesGroup):
    password = State()
    request = State()
    attempts_limit = State()

class MainMenu(StatesGroup):
    main = State()
    widget = State()
    cell = State()
