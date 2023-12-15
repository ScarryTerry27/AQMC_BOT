from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопка отмены
button_cancel = KeyboardButton('Отмена')
# клавиатура отмены
kb_cancel = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True).add(button_cancel)

# Кнопки выбора отделений
b1 = KeyboardButton('1 гинекологическое')
b2 = KeyboardButton('2 гинекологическое')
b3 = KeyboardButton('Детское гинекологическое')
b4 = KeyboardButton('Физиологическое акушерское')
b5 = KeyboardButton('Обсервационное акушерское')
b6 = KeyboardButton('Отделение патологии беременности')
b7 = KeyboardButton('Родильный блок')
b8 = KeyboardButton('Реанимация')
b9 = KeyboardButton('Приемное', callback_data='choice_po')
b10 = KeyboardButton('Анестезиология', callback_data='choice_anest')

# Клавиатура выбора отделений
unit_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
unit_kb.row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(button_cancel)

# Клавиатура выбора отделений + 2 отделения
unit_kb_upgrade = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
unit_kb_upgrade.row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10).row(button_cancel)

# кнопки и клавиатура, узнаем как доставлена в клинику
r1 = KeyboardButton('По направлению из женской консультации')
r2 = KeyboardButton('Привезла скорая помощь')
r3 = KeyboardButton('По направлению из другого медицинского учреждения')
r4 = KeyboardButton('Самообращение')
r5 = KeyboardButton('Затрудняюсь ответить')

ref_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
ref_kb.row(r1, r2).row(r3).row(r4, r5).row(button_cancel)

# кнопки и клавиатура, узнаем почему выбрала клинику
rr1 = KeyboardButton('Ближе к дому')
rr2 = KeyboardButton('Посоветовали близкие/знакомые')
rr3 = KeyboardButton('Порекомендовали в другом медицинском учреждении')
rr4 = KeyboardButton('Увидела вашу рекламу')
rr5 = KeyboardButton('Не нашла альтернативы')
res_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
res_kb.row(rr1, rr2).row(rr3, rr4).row(rr5).row(button_cancel)


#  оказание помощи оценка качества
# кнопки и клавиатура, градация от 1 до 10
kb1 = KeyboardButton('1 - ' + '\U0001F630')
kb2 = KeyboardButton('2 - ' + '\U0001F622')
kb3 = KeyboardButton('3 - ' + '\U0001F61F')
kb4 = KeyboardButton('4 - ' + '\U00002639')
kb5 = KeyboardButton('5 - ' + '\U0001F641')
kb6 = KeyboardButton('6 - ' + '\U0001F610')
kb7 = KeyboardButton('7 - ' + '\U0001F642')
kb8 = KeyboardButton('8 - ' + '\U0001F60A')
kb9 = KeyboardButton('9 - ' + '\U0001F600')
kb10 = KeyboardButton('10 - ' + '\U0001F604')

scale1_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
scale1_kb.row(kb1, kb2, kb3, kb4, kb5).row(kb6, kb7, kb8, kb9, kb10).row(button_cancel)

# кнопки и клавиатура, да/нет

binar_kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
but1 = KeyboardButton('Да - ' + '\U00002714')
but2 = KeyboardButton('Нет - ' + '\U0000274C')
binar_kb.row(but1, but2).row(button_cancel)
