from aiogram import Dispatcher, types


async def help(message: types.Message):
    await message.answer("Этот бот создан для удаленного управления контроллером wirenboard\n"
                   "Чтобы пройти регистрацию или начать работу нажмите /start\n"
                   "Это сообщение будет дополняться по мере добавления функционала")
    
def register_help(dp: Dispatcher):
    dp.register_message_handler(help, commands="help", state="*")