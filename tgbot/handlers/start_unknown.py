from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit
from tgbot.keyboards.new_user import registration_keyboard, registration_callback
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import NewUser
from tgbot.config import load_config, add_admin
from tgbot.utils.db_api.sqlite import Database
from bot import bot
from bot import logger

db = Database()
config = load_config(".env")

@rate_limit(limit=1)
async def start_unknown(message: types.Message, user: User):
    await message.answer(f"Здравствуй, {user.name}. Я тебя не знаю. Введи пароль доступа или отправь запрос администратору", reply_markup=registration_keyboard)


async def enter_password(cq: types.CallbackQuery, callback_data: dict):
    logger.info("function enter_password")
    await cq.answer()
    await cq.message.answer("Введите пароль")
    await NewUser.password.set()

async def get_password(message: types.Message, state=FSMContext):
    logger.info("function get password")
    password = int(message.text)
    if password == config.tg_bot.admin_password:
        add_admin(message.from_user.id)
        db.update_status(status="ADMIN", id=message.from_user.id)
        await state.finish()
    else:
        await message.answer("Неверный пароль. Попробуй еще раз")
        async with state.proxy() as data:
            data["tryes"] = 0
        data["tryes"] += 1
        if data["tryes"] == 4:
            await message.answer("Осталась последняя попытка")
        if data["tryes"] == 5:
            await message.answer("Все, хватит. Думаю ты не знаешь пароль")
            await state.finish()
        await NewUser.password.set()


def register_unknown(dp: Dispatcher):
    dp.register_message_handler(start_unknown, commands=["start"], state="*")
    dp.register_callback_query_handler(enter_password,
        registration_callback.filter(choice="enter_password"))
    dp.register_message_handler(get_password, state=NewUser.password)
    # dp.register_callback_query_handler(
    #     registration_callback.filter(choice="send_request"))
    # dp.register_callback_query_handler(
    #     registration_callback.filter(choise="cancel"))
