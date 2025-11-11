from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from tgbot.keyboards.main_keyboard import main_callback, MainKeyboard, AdminKeyboard
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from loader import  bot, config
from tgbot.utils.db_api.db_commands import Database 
import re
# from javascript import require
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.keyboards.callback_datas import widgets_callback, cells_callback
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import MainMenu

# device = require("/mnt/data/SmartHome/wb-rules-modules/")
# device = require("/home/siddha/SmartHome/wb-rules-modules/cell.js")

db = Database()
main_kbd = MainKeyboard()
admin_kbd = AdminKeyboard()


   
async def get_widgets(cq: CallbackQuery):
    """
    Handler for mangind devices placed in certain rooom.

    Arguments:
    - cq (types.CallbackQuery): The callback query object.
    - state (FSMContext): The FSM context.
    """
    with open(config.tg_bot.dashboards) as f:
        dashboard = json.load(f)
    keyboard = InlineKeyboardMarkup()
    for widget in dashboard['widgets']:
        text = widget['name']
        callback_data = widgets_callback.new(command=widget['id'])
        keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))
    keyboard.add(InlineKeyboardButton('Назад', callback_data=widgets_callback.new(command='return')))
    await cq.message.edit_text(text='Виджеты')
    await cq.message.edit_reply_markup(reply_markup=keyboard)
    await MainMenu.cell.set()

async def back_to_main(cq: CallbackQuery, state:FSMContext):
    await cq.message.edit_text(text='Меню')
    keyboard = keyboard_constructor(main_kbd.get_widgets, main_kbd.devices)
    user = db.get_user(id=cq.from_user.id)
    if user.status == 'ADMIN':
        keyboard.add(main_kbd.settings)
        keyboard.add(main_kbd.system)
        keyboard.add(admin_kbd.get_users)
    await cq.message.edit_reply_markup(reply_markup=keyboard)
    await state.finish()
    
async def get_cell(cq: CallbackQuery, state: FSMContext):
    with open(config.tg_bot.dashboards) as f:
        dashboard = json.load(f)
    keyboard = InlineKeyboardMarkup()
    for widget in dashboard['widgets']:
        if widget['id'] == cq.data.split(':')[1]:
            name = widget['name']
            await cq.message.edit_text(name)
            # value = device.getValue()
            value = 1
            for cell in widget['cells']:
                try:
                    text = cell['name']
                    if text == "":
                        continue
                    if text == "working on battery":
                        if value:
                            text += ' 🔋'
                        else:
                            text += ' 🪫'
                    else:
                        if cell['type'] == 'switch' or 'alarm':# or 'pushbutton' or 'range':
                            if value:
                                text += ' ✅'
                            else:
                                text += ' ⭕️'
                        elif cell['type'] == 'pushbutton':
                            text += ' 🖲'
                        else:
                            text += f" {value} {cell['type']}"
                    callback_data = cells_callback.new(command=cell['id'])
                    keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))  
                except Exception:
                    continue
                #    await cq.answer("Ошибка параметр 'name' не найден", show_alert=True)
    keyboard.add(InlineKeyboardButton('Назад', callback_data=cells_callback.new(command='return')))
    await cq.message.edit_reply_markup(keyboard)
    await state.finish()

async def get_users(cq: CallbackQuery):
    users = db.get_all_users()
    text = ''
    keyboard = InlineKeyboardMarkup(1)
    for user in users:
        text += f'id = {user[0]}, Имя: {user[2]}, Статус: {user[3]}\n'
    await cq.message.edit_text(text) 
    keyboard.add(InlineKeyboardButton('Назад', callback_data=widgets_callback.new(command='return')))
    await cq.message.edit_reply_markup(reply_markup=keyboard)

def register_common(dp: Dispatcher):
    """
    Function to register the admin start command handler with the dispatcher.

    Arguments:
    - dp (Dispatcher): The dispatcher object.
    """
    
    dp.register_callback_query_handler(get_widgets, main_callback.filter(command="get_widgets"))
    dp.register_callback_query_handler(back_to_main, widgets_callback.filter(command="return"), state="*")
    dp.register_callback_query_handler(get_widgets, cells_callback.filter(command="return"))
    dp.register_callback_query_handler(get_cell, state=MainMenu.cell)
    dp.register_callback_query_handler(get_users, main_callback.filter(command="get_users"))
