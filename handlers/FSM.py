from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from date_base.sqlite_db import sql_add_command, check_id, sql_delete_command, sql_add_command_quality_oms, \
    sql_add_command_quality_dms
from keyboards.client_inline import kb_main
from keyboards.client_kb import unit_kb, ref_kb, res_kb, scale1_kb, binar_kb, unit_kb_upgrade

dicti = {
        '1 - ' + '\U0001F630': 1, '2 - ' + '\U0001F622': 2, '3 - ' + '\U0001F61F': 3,
        '4 - ' + '\U00002639': 4, '5 - ' + '\U0001F641': 5, '6 - ' + '\U0001F610': 6,
        '7 - ' + '\U0001F642': 7, '8 - ' + '\U0001F60A': 8, '9 - ' + '\U0001F600': 9,
        '10 - ' + '\U0001F604': 10
        }

d = {
    'Да - ' + '\U00002714': 1,
    'Нет - ' + '\U0000274C': 2
}


# Класс заполнение формы
class FSMgeneral(StatesGroup):
    unit = State()
    count_days = State()
    referral = State()
    reason = State()


# Класс для оценки качества ОМС
class FSMoms(StatesGroup):
    unit = State()
    conditions = State()   # условия в приемке
    diagnostics = State()   # диагностика
    free_medicines = State()  # бесплатные лекарства
    information = State()  # доступность информации
    doctor = State()    # врачи
    nurse = State()     # мед сестры
    orderly = State()   # санитары
    placement = State()  # размещение
    nutrition = State()  # питание
    treatment = State()  # лечение
    general = State()   # общее впечатление


# Класс для оценки качества ДМС
class FSMdms(StatesGroup):
    consultation = State()   # консультации
    operation = State()   # операция
    anesthesia = State()  # анестезия
    other = State()  # др.манипуляции
    diagnostics = State()    # диагностика
    analyzes = State()     # анализы
    devices = State()   # сложные изделия
    simple_devices = State()  # простые изделия
    drugs = State()  # таблетки
    hygienic = State()  # гигиена
    ward = State()   # палата
    nothing = State()  # ничего


async def cancel_handler(message: Message, state: (FSMContext or FSMoms or FSMdms)):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.reply('Вы отменили заполнение формы\n\n\nГлавное меню', reply_markup=kb_main)


# Функции Заполнения первоначальной формы
async def fill_gen_form(callback_query: CallbackQuery):
    await FSMgeneral.unit.set()
    await bot.send_message(callback_query.from_user.id, 'Выберите ваше отделение', reply_markup=unit_kb)


async def load_unit(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['unit'] = message.text
    await FSMgeneral.next()
    await message.reply('Введите номер истории болезни')


async def load_count_days(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['medical_case'] = message.text
    await FSMgeneral.next()
    await message.reply('Как вы попали к нам в больницу?', reply_markup=ref_kb)


async def load_referral(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['referral'] = message.text
        data['reason'] = '0'
    if message.text == 'Самообращение':
        await FSMgeneral.next()
        await message.reply('Почему вы выбрали нашу клинику?', reply_markup=res_kb)
    else:
        if check_id(message.from_user.id):
            await sql_delete_command(message.from_user.id)
        await sql_add_command(state)
        await state.finish()
        await message.reply('Форма успешно заполнена\n\n\nГлавное меню', reply_markup=kb_main)


async def load_reason(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    if check_id(message.from_user.id):
        await sql_delete_command(message.from_user.id)
    await sql_add_command(state)
    await state.finish()
    await message.reply('Форма успешно заполнена\n\n\nГлавное меню', reply_markup=kb_main)


# Функции для оценки качества ОМС
async def fill_oms(callback_query: CallbackQuery):
    await FSMoms.unit.set()
    await bot.send_message(callback_query.from_user.id, 'Какое отделение вы бы хотели оценить?',
                           reply_markup=unit_kb_upgrade)


async def load_unit1(message: Message, state: FSMoms):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['unit'] = message.text
    await FSMoms.next()
    await message.reply('Оцените условия оказания медицинской помощи в приемном отделении от 1 до 10',
                        reply_markup=scale1_kb)


async def load_conditions(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['conditions'] = dicti[message.text]
        else:
            data['conditions'] = 0
    await FSMoms.next()
    await message.reply('Оцените доступность и качество диагностических исследований от 1 до 10',
                        reply_markup=scale1_kb)


async def load_diagnostics(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['diagnostics'] = dicti[message.text]
        else:
            data['diagnostics'] = 0
    await FSMoms.next()
    await message.reply('Оцените обеспечение бесплатными лекарственными препаратами от 1 до 10',
                        reply_markup=scale1_kb)


async def load_free_medicines(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['free_medicines'] = dicti[message.text]
        else:
            data['free_medicines'] = 0
    await FSMoms.next()
    await message.reply('Оцените доступность и качество информации, полученной от Вашего лечащего врача от 1 до 10',
                        reply_markup=scale1_kb)


async def load_information(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['information'] = dicti[message.text]
        else:
            data['information'] = 0
    await FSMoms.next()
    await message.reply('Оцените работу врачей от 1 до 10',
                        reply_markup=scale1_kb)


async def load_doctor(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['doctor'] = dicti[message.text]
        else:
            data['doctor'] = 0
    await FSMoms.next()
    await message.reply('Оцените работу медсестер от 1 до 10',
                        reply_markup=scale1_kb)


async def load_nurse(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['nurse'] = dicti[message.text]
        else:
            data['nurse'] = 0
    await FSMoms.next()
    await message.reply('Оцените работу санитаров от 1 до 10',
                        reply_markup=scale1_kb)


async def load_orderly(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['orderly'] = dicti[message.text]
        else:
            data['orderly'] = 0
    await FSMoms.next()
    await message.reply('Оцените условия бесплатного размещения от 1 до 10',
                        reply_markup=scale1_kb)


async def load_placement(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['placement'] = dicti[message.text]
        else:
            data['placement'] = 0
    await FSMoms.next()
    await message.reply('Оцените качество питания от 1 до 10',
                        reply_markup=scale1_kb)


async def load_nutrition(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['nutrition'] = dicti[message.text]
        else:
            data['nutrition'] = 0
    await FSMoms.next()
    await message.reply('Оцените результаты лечения от 1 до 10',
                        reply_markup=scale1_kb)


async def load_treatment(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['treatment'] = dicti[message.text]
        else:
            data['treatment'] = 0
    await FSMoms.next()
    await message.reply('Оцените в целом лечение в больнице от 1 до 10',
                        reply_markup=scale1_kb)


async def load_general(message: Message, state: FSMoms):
    async with state.proxy() as data:
        if message.text in dicti.keys():
            data['general'] = dicti[message.text]
        else:
            data['general'] = 0
    await sql_add_command_quality_oms(state)
    await state.finish()
    await message.reply('Форма успешно заполнена\n\n\nГлавное меню', reply_markup=kb_main)


# Функции для оценки качества ДМС
async def fill_dms(callback_query: CallbackQuery):
    await FSMdms.consultation.set()
    await bot.send_message(
        callback_query.from_user.id, 'Я оплачивала консультацию врачей-специалистов',
        reply_markup=binar_kb)


async def load_consultation(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['consultation'] = d[message.text]
    await FSMdms.next()
    await message.reply('Я оплачивала операцию',
                        reply_markup=binar_kb)


async def load_operation(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['operation'] = d[message.text]
    await FSMdms.next()
    await message.reply('Я оплачивала общее обезболивание (наркоз) или местную анестезию',
                        reply_markup=binar_kb)


async def load_anesthesia(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['anesthesia'] = d[message.text]
    await FSMdms.next()
    await message.reply('Я оплачивала другие медицинские манипуляции (перевязки, инъекции и тп)',
                        reply_markup=binar_kb)


async def load_other(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['other'] = d[message.text]
    await FSMdms.next()
    await message.reply('Я оплачивала инструментальные диагностические исследования (ЭКГ, УЗИ, рентген, МРТ, КТ и пр.',
                        reply_markup=binar_kb)


async def load_diagnostics_dms(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['diagnostics'] = d[message.text]
    await FSMdms.next()
    await message.reply('Я оплачивала лабораторные исследования (анализы)',
                        reply_markup=binar_kb)


async def load_analyzes(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['analyzes'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я оплачивала сложные изделия медицинского назначения 
    (эндопротезы, кардиостимуляторы, искусственные хрусталики и пр.''',
                        reply_markup=binar_kb)


async def load_devices(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['devices'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я оплачивала простые изделия медицинского назначения 
    (бинты, шприцы, памперсы, простыни и пр.''',
                        reply_markup=binar_kb)


async def load_simple_devices(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['simple_devices'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я оплачивала лекарства (таблетки, препараты для инъекций и капельниц и пр.''',
                        reply_markup=binar_kb)


async def load_drugs(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['drugs'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я оплачивала гигиенические услуги по уходу''',
                        reply_markup=binar_kb)


async def load_hygienic(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['hygienic'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я оплачивала размещение в палате повышенное комфортности''',
                        reply_markup=binar_kb)


async def load_ward(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['ward'] = d[message.text]
    await FSMdms.next()
    await message.reply('''Я ничего оплачивала и не покупала''',
                        reply_markup=binar_kb)


async def load_nothing(message: Message, state: FSMdms):
    async with state.proxy() as data:
        data['nothing'] = d[message.text]
    await sql_add_command_quality_dms(state)
    await state.finish()
    await message.reply('Форма успешно заполнена\n\n\nГлавное меню', reply_markup=kb_main)


def registers_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_callback_query_handler(fill_gen_form, Text(endswith='fill_form_gen'), state=None)
    dp.register_message_handler(load_unit, state=FSMgeneral.unit)
    dp.register_message_handler(load_count_days, state=FSMgeneral.count_days)
    dp.register_message_handler(load_referral, state=FSMgeneral.referral)
    dp.register_message_handler(load_reason, state=FSMgeneral.reason)
    # регистрация функций для оценки качества ОМС
    dp.register_callback_query_handler(fill_oms, Text(endswith='OMS'), state=None)
    dp.register_message_handler(load_unit1, state=FSMoms.unit)
    dp.register_message_handler(load_conditions, state=FSMoms.conditions)
    dp.register_message_handler(load_diagnostics, state=FSMoms.diagnostics)
    dp.register_message_handler(load_free_medicines, state=FSMoms.free_medicines)
    dp.register_message_handler(load_information, state=FSMoms.information)
    dp.register_message_handler(load_doctor, state=FSMoms.doctor)
    dp.register_message_handler(load_nurse, state=FSMoms.nurse)
    dp.register_message_handler(load_orderly, state=FSMoms.orderly)
    dp.register_message_handler(load_placement, state=FSMoms.placement)
    dp.register_message_handler(load_nutrition, state=FSMoms.nutrition)
    dp.register_message_handler(load_treatment, state=FSMoms.treatment)
    dp.register_message_handler(load_general, state=FSMoms.general)
    # регистрация функций для оценки качества ДМС
    dp.register_callback_query_handler(fill_dms, Text(endswith='DMS'), state=None)
    dp.register_message_handler(load_consultation, state=FSMdms.consultation)
    dp.register_message_handler(load_operation, state=FSMdms.operation)
    dp.register_message_handler(load_anesthesia, state=FSMdms.anesthesia)
    dp.register_message_handler(load_other, state=FSMdms.other)
    dp.register_message_handler(load_diagnostics_dms, state=FSMdms.diagnostics)
    dp.register_message_handler(load_analyzes, state=FSMdms.analyzes)
    dp.register_message_handler(load_devices, state=FSMdms.devices)
    dp.register_message_handler(load_simple_devices, state=FSMdms.simple_devices)
    dp.register_message_handler(load_drugs, state=FSMdms.drugs)
    dp.register_message_handler(load_hygienic, state=FSMdms.hygienic)
    dp.register_message_handler(load_ward, state=FSMdms.ward)
    dp.register_message_handler(load_nothing, state=FSMdms.nothing)




