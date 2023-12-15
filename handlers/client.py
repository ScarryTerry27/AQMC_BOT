from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from date_base.sqlite_db import check_id
from keyboards.client_inline import form_kb, kb_main, kb_qt


# commands=['start']
async def command_start(message: Message):
    try:
        if not check_id(message.from_user.id):
            await bot.send_message(message.from_user.id,
                               text='Для работы с ботом для начала заполните форму',
                               reply_markup=form_kb)
        else:
            await bot.send_message(message.from_user.id,
                                   text='Выберите действие',
                                   reply_markup=kb_main)
    except:
        await message.reply('Сначала напиши в лс боту\nhttps://t.me/ScaryTerryBot')


async def choice_quality(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'По какому полису вы получали услуги',
                           reply_markup=kb_qt)


def registers_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(choice_quality, Text(startswith='quality'))
