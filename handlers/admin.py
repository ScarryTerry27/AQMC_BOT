from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from date_base import sqlite_db
from config import admin_ids
from create_bot import bot
from date_base.sqlite_db import sql_read_gen_info, sql_read_dms, sql_read_oms
from keyboards.admin_kb import button_case_admin, db_admin_kb


async def message_admins(dp):
    print('Бот запущен')
    sqlite_db.sql_start()
    for ad in admin_ids:
        await bot.send_message(int(ad), text='Бот онлайн')


async def moderator_command(message: Message):
    if str(message.from_user.id) in admin_ids:
        await bot.send_message(message.from_user.id, text='Выберите действие', reply_markup=button_case_admin)


async def command_read(callback_query: CallbackQuery):
    if str(callback_query.from_user.id) in admin_ids:
        await bot.send_message(callback_query.from_user.id, text='Из какой базы прочитать данные?',
                               reply_markup=db_admin_kb)


async def command_gen_info(message: Message):
    if str(message.from_user.id) in admin_ids:
        await sql_read_gen_info(message)


async def command_read_oms(message: Message):
    if str(message.from_user.id) in admin_ids:
        await sql_read_oms(message)


async def command_read_dms(message: Message):
    if str(message.from_user.id) in admin_ids:
        await sql_read_dms(message)


def registers_handlers_admin(dp: Dispatcher):  # регистрируем хендлеры
    dp.register_message_handler(moderator_command, commands=['moderator'])
    dp.register_callback_query_handler(command_read, Text(startswith='read_sql'))
    dp.register_message_handler(command_gen_info, Text(endswith='Прочитать общую информацию о пациентах'))
    dp.register_message_handler(command_read_oms, Text(endswith='Прочитать ОМС'))
    dp.register_message_handler(command_read_dms, Text(endswith='Прочитать ДМС'))


