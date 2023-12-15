import json
import string
from aiogram import Dispatcher
from aiogram.types import Message


async def echo_send(message: Message):
    # цензура
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()}\
            .intersection(set(json.load(open('mat.json')))):
        await message.reply('Не ругайся')
        await message.delete()


# @dp.inline_handler()
# async def inline_handler(query: types.InlineQuery):
#     text = query.query or 'echo'
#     link = 'https://gufo.me/dict/rude/' + text
#     result_id: str = hashlib.md5(text.encode()).hexdigest()
#
#     articles = [InlineQueryResultArticle(id=result_id, title='Русско-немецкий словарь', url=link,
#                                          input_message_content=InputTextMessageContent(message_text=link))]
#     await query.answer(articles, cache_time=1, is_personal=True)


def registers_handlers_other(dp: Dispatcher):  # регистрируем хендлеры
    dp.register_message_handler(echo_send)
