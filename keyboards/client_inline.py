from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

a1 = InlineKeyboardButton(text='Оценить качество оказания помощи', callback_data='quality')
a2 = InlineKeyboardButton(text='Обновить форму', callback_data='fill_form_gen')

kb_main = InlineKeyboardMarkup(row_width=2).add(a1).add(a2)

form_kb = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Заполнить форму', callback_data='fill_form_gen'),
)

c1 = InlineKeyboardButton(text='По полису ОМС', callback_data='OMS')
c2 = InlineKeyboardButton(text='По полису ДМС', callback_data='DMS')
kb_qt = InlineKeyboardMarkup(row_width=2).row(c1, c2)

b1 = InlineKeyboardButton('1 гинекологическое', callback_data='choice_1go')
b2 = InlineKeyboardButton('2 гинекологическое', callback_data='choice_2go')
b3 = InlineKeyboardButton('Детское гинекологическое', callback_data='choice_dgo')
b4 = InlineKeyboardButton('Физиологическое акушерское', callback_data='choice_fao')
b5 = InlineKeyboardButton('Обсервационное акушерское', callback_data='choice_oao')
b6 = InlineKeyboardButton('Отделение патологии беременности', callback_data='choice_opb')
b7 = InlineKeyboardButton('Родильный блок', callback_data='choice_rb')
b8 = InlineKeyboardButton('Реанимация', callback_data='choice_rean')
b9 = InlineKeyboardButton('Приемное', callback_data='choice_po')
b10 = InlineKeyboardButton('Анестезиология', callback_data='choice_anest')
unit_inline_kb = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
unit_inline_kb.row(b1, b2, b3).row(b4, b5, b6).row(b7, b8, b9, b10)
