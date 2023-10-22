import re
from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.keyboards.registration_keyboard import registration_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import NewUser
from loader import config, bot
from tgbot.utils.db_api.db_commands import Database 
import datetime

db = Database()
btn = Button()
ATTEMPTS = 3 # Количество попыток ввода пароля
TIMEOUT = 30 # Таймаут после израсходования попыток

async def start_unknown(message: types.Message, user: User, state: FSMContext):
    """
    Handler for the start command when the user is unknown.

    Arguments:
    - message (types.Message): The message object.
    - user (User): The user object.
    - state (FSMContext): The FSM context.
    """

    await message.answer(f"Здравствуй, {user.name}. Я тебя не знаю. Введи пароль доступа или отправь запрос администратору",
                         reply_markup=keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    await state.reset_state(with_data=False)
    async with state.proxy() as data:
        data["attempts"] = 0
        data["time"] = 0


async def enter_password(cq: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Handler for entering the admin password.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - callback_data (dict): The callback data.
    - state (FSMContext): The FSM context.
    """

    await cq.answer()
    await cq.message.edit_text("Введите пароль", reply_markup=keyboard_constructor(btn.cancel))
    await NewUser.password.set()


async def get_password(message: types.Message, state: FSMContext):
    """
    Handler for getting the admin password and checking its validity.

    Arguments:
    - message (types.Message): The message object.
    - state (FSMContext): The FSM context.
    """

    password = int(message.text)
    if password == config.tg_bot.admin_password:
        db.update_status(message.from_user.id, "ADMIN")
        await state.finish()
        await message.answer("Пароль принят! Вы зарегистрированы как администратор.\n"
                             "Для начала работы отправьте /start")
    else:
        data = await state.get_data()
        attempt = data.get("attempts")
        attempt = attempt + 1
        data["attempts"] = attempt
        await state.update_data(data=data, kwargs="attempts")
        if attempt > ATTEMPTS - 1:
            now = datetime.datetime.now()
            delta = now + datetime.timedelta(minutes=TIMEOUT)
            data["time"] = delta
            await state.update_data(data=data, kwargs=("time"))
            await message.answer("Все, хватит. Думаю ты не знаешь пароль",
                                 reply_markup=keyboard_constructor(btn.send_request, btn.cancel))
            await NewUser.attempts_limit.set()
            print(await state.get_state())
            print(data)
        elif attempt == ATTEMPTS - 1:
            await message.answer("Осталась последняя попытка", reply_markup=keyboard_constructor(btn.cancel))
            await NewUser.password.set()
        else:
            await message.answer(f"Неверный пароль. Осталось попыток: {ATTEMPTS-attempt}", reply_markup=keyboard_constructor(btn.cancel))
            await NewUser.password.set()


async def send_request(cq: types.CallbackQuery, user: User):
    """
    Handler for sending a request to the administrators for access.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - user (User): The user object.
    """

    admins = db.get_admins()
    if not admins:        
        await cq.answer()
        await cq.message.edit_text("Упс, похоже здесь еще нет ни одного администратора... Попробуйте ввести пароль.", 
                                reply_markup=keyboard_constructor(btn.enter_password, btn.cancel))
    else:
        for admin in admins:
            await bot.send_message(admin.id, f"Пользователь {user.name} хочет получить доступ к боту. ID={user.id}", 
                                reply_markup=keyboard_constructor(btn.accept, btn.make_admin, btn.refuse))
            await cq.answer(text="Запрос отправлен администратору", show_alert=True)
            await NewUser.request.set()


async def request_sent(message: types.Message):
    """
    Handler for informing the user that their request has been sent.

    Arguments:
    - message (types.Message): The message object.
    """

    await message.answer("Вы уже отправили запрос. Имейте терпение, скоро администратор рассмотрит его")


async def attempts_limit(message: types.Message, state: FSMContext):
    """
    Handler for informing the user about the attempts limit.

    Arguments:
    - message (types.Message): The message object.
    - state (FSMContext): The FSM context.
    """

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
    """
    Handler for debugging purposes.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - state (FSMContext): The FSM context.
    """

    await state.reset_state(with_data=True)
    await cq.answer("Data reset")


async def cancel(cq: types.CallbackQuery, state: FSMContext):
    """
    Handler for canceling the current operation.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - state (FSMContext): The FSM context.
    """

    await cq.message.edit_text(f"Введи пароль доступа или отправь запрос администратору")
    await cq.message.edit_reply_markup(keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    await cq.answer(text="Всего хорошего!", show_alert=True)
    await state.reset_state(with_data=False)


def register_unknown(dp: Dispatcher):
    """
    Register handlers for the unknown user state.

    Arguments:
    - dp (Dispatcher): The dispatcher object.
    """

    dp.register_message_handler(start_unknown, commands=["start"], state="*")
    dp.register_callback_query_handler(debug, registration_callback.filter(reg="debug"), state="*")
    dp.register_message_handler(attempts_limit, state=NewUser.attempts_limit)
    dp.register_callback_query_handler(cancel, registration_callback.filter(reg="cancel"), state="*")
    dp.register_callback_query_handler(enter_password, registration_callback.filter(reg="enter_password"))
    dp.register_message_handler(get_password, state=NewUser.password)
    dp.register_callback_query_handler(send_request, registration_callback.filter(reg="send_request"))
    dp.register_message_handler(request_sent, state=NewUser.request)
