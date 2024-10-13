from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from tgbot.keyboards.main_keyboard import main_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from loader import  bot, config
from tgbot.utils.db_api.db_commands import Database 
import re
from javascript import require
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.keyboards.callback_datas import widgets_callback, cells_callback
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import MainMenu
from emoji import emojize

# dashboard = require("/mnt/data/SmartHome/wb-rules-modules/")
cell = require("/home/siddha/SmartHome/wb-rules-modules/cell.js")

db = Database()
btn = Button()


   
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
    await cq.message.edit_reply_markup(reply_markup=keyboard_constructor(btn.get_widgets, btn.devices, btn.settings, btn.system))
    await state.finish()
    
async def get_cell(cq: CallbackQuery, state: FSMContext):
    with open(config.tg_bot.dashboards) as f:
        dashboard = json.load(f)
    keyboard = InlineKeyboardMarkup(2)
    for widget in dashboard['widgets']:
        if widget['id'] == cq.data.split(':')[1]:
            name = widget['name']
            await cq.message.edit_text(name)
            for cell in widget['cells']:
                try:
                    text = cell['name']
                    cell(cell['id'])
                    value = cell.getValue()
                    if cell['type'] == 'switch' or 'alarm':# or 'pushbutton' or 'range':
                        if value:
                            emoji = emojize()
                        
                    callback_data = cells_callback.new(command=cell['id'])
                    keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))  
                except Exception:
                    cq.answer("Ошибка параметр 'name' не найден", show_alert=True)
    keyboard.add(InlineKeyboardButton('Назад', callback_data=cells_callback.new(command='return')))
    await cq.message.edit_reply_markup(keyboard)
    await state.finish()
    
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