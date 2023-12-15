from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = InlineKeyboardButton('Прочитать данные опросов', callback_data='read_sql')
button_delete = InlineKeyboardButton('Удалить данные опросов', callback_data='del_sql')

button_case_admin = InlineKeyboardMarkup(row_width=2).row(button_load, button_delete)

b1 = KeyboardButton('Прочитать общую информацию о пациентах')
b2 = KeyboardButton('Прочитать ОМС')
b3 = KeyboardButton('Прочитать ДМС')

db_admin_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True).row(b1, b2, b3)
