from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import Test


async def enter_test(message: types.Message):
    await message.answer("начало тестирования. \n"
                         "Вопрос №1")

    await Test.q1.set()


async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    async with state.proxy() as data:
        data["answer1"] = answer

    await message.answer(f"ваш ответ: {data['answer1']}.\n"
                         "вопрос №2...")
    await Test.q2.set()


async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text

    await message.answer(f"ваш ответ: {answer2}.")
    await message.answer(f"предыдущий ответ: {answer1}.")

    # await state.finish()
    await state.reset_state(with_data=False)


def register_test(dp: Dispatcher):
    dp.register_message_handler(enter_test, Command("test"))
    dp.register_message_handler(answer_q1, state=Test.q1)
    dp.register_message_handler(answer_q2, state=Test.q2)
