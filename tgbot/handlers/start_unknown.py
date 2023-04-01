import re
from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit
from tgbot.keyboards.registration_keyboard import registration_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import NewUser
from tgbot.config import load_config, add_admin
from tgbot.utils.db_api.sqlite import Database
from app import bot
import datetime

db = Database()
config = load_config()
btn = Button()


@rate_limit(limit=1)
async def start_unknown(message: types.Message, user: User, state: FSMContext):
    await message.answer(f"Здравствуй, {user.name}. Я тебя не знаю. Введи пароль доступа или отправь запрос администратору",
                         reply_markup=keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    await state.reset_state(with_data=False)
    async with state.proxy() as data:
        data["attempts"] = 0
        data["time"] = 0


async def enter_password(cq: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await cq.answer()
    await cq.message.answer("Введите пароль", reply_markup=keyboard_constructor(btn.cancel))
    await NewUser.password.set()


async def get_password(message: types.Message, state: FSMContext):
    password = int(message.text)
    if password == config.tg_bot.admin_password:
        add_admin(message.from_user.id)
        await state.finish()
        await message.answer("Пароль принят! Вы зарегистрированы как администратор.\n"
                             "Для начала работы отправьте /start")
    else:
        data = await state.get_data()
        attempt = data.get("attempts")
        attempt = attempt + 1
        data["attempts"] = attempt
        await state.update_data(data=data, kwargs="attempts")
        if attempt > 2:
            now = datetime.datetime.now()
            delta = now + datetime.timedelta(minutes=30)
            data["time"] = delta
            await state.update_data(data=data, kwargs=("time"))
            await message.answer("Все, хватит. Думаю ты не знаешь пароль",
                                 reply_markup=keyboard_constructor(btn.send_request, btn.cancel))
            await NewUser.attempts_limit.set()
            print(await state.get_state())
            print(data)
        elif attempt == 2:
            await message.answer("Осталась последняя попытка", reply_markup=keyboard_constructor(btn.cancel))
            await NewUser.password.set()
        else:
            await message.answer(f"Неверный пароль. Осталось попыток: {3-attempt}", reply_markup=keyboard_constructor(btn.cancel))
            await NewUser.password.set()


async def send_request(cq: types.CallbackQuery, user: User):
    if not config.tg_bot.admin_ids:        
        await cq.answer()
        await cq.message.answer("Упс, похоже здесь еще нет ни одного администратора... Попробуйте ввести пароль.", 
                                reply_markup=keyboard_constructor(btn.enter_password, btn.cancel))
    else:
        for id in config.tg_bot.admin_ids:
            await bot.send_message(id, f"Пользователь {user.name} хочет получить доступ к боту. ID={user.id}", 
                                reply_markup=keyboard_constructor(btn.accept, btn.make_admin, btn.refuse))
            await cq.answer(text="Запрос отправлен администратору")
            await NewUser.request.set()

async def request_sent(message: types.Message):
    await message.answer("Вы уже отправили запрос. Имейте терпение, скоро администратор рассмотрит его")

async def attempts_limit(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        print(data)
        time = data.get("time")
        print(time)
        now = datetime.datetime.now()
        now.minute
        time.minute
        print(time - now)
        if now >= time:
            await state.reset_data()
        else:
            remain = str(time - now)
            output = re.findall(r':[0-9]{2}:', remain)
            result = output[0][1:-1]
            print(result)
            await message.answer(f"Попробуйте еще через {result} минут.", reply_markup=keyboard_constructor(btn.debug))
    except:
        pass

async def debug(cq: types.CallbackQuery, state:FSMContext):
    await state.reset_state(with_data=True)
    await cq.answer("Data reset")

async def cancel(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_text(f"Введи пароль доступа или отправь запрос администратору")
    await cq.message.edit_reply_markup(keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    await cq.answer(text="Всего хорошего!", show_alert=True)
    await state.reset_state(with_data=False)


def register_unknown(dp: Dispatcher):
    dp.register_message_handler(start_unknown, commands=["start"], state="*")
    dp.register_callback_query_handler(debug, registration_callback.filter(reg="debug"), state="*")
    dp.register_message_handler(attempts_limit, state=NewUser.attempts_limit)
    dp.register_callback_query_handler(cancel, registration_callback.filter(reg="cancel"), state="*")
    dp.register_callback_query_handler(enter_password, registration_callback.filter(reg="enter_password"))
    dp.register_message_handler(get_password, state=NewUser.password)
    dp.register_callback_query_handler(send_request, registration_callback.filter(reg="send_request"))
    dp.register_message_handler(request_sent, state=NewUser.request)
