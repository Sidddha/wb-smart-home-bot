from aiogram import Dispatcher, types


async def help(message: types.Message):
    message.answer("Этот бот создан для удаленного управления контроллером wirenboard\n"
                   "Чтобы пройти регистрацию нажмите /start\n"
                   )