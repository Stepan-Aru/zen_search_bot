from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tokens import telegram_bot_token
from zen import get_articles

bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)


help_text = 'Напиши мне запрос и количествой статей для выдачи.\n' \
            'Например так: Котики 5'

@dp.message_handler(commands=['start', 'help'])
async def send_welcome_info(msg: types.Message):
    await msg.reply(f'Привет, {msg.from_user.first_name}!\n'
                    f'Я могу найти для тебя статьи в zen.\n{help_text}')


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    await msg.answer('Начинаю поиск...')
    try:
        msg_lst = msg.text.lower().split()
        if msg_lst[-1].isdigit() and msg_lst[-2].isdigit():
            search = ' '.join(msg_lst[:-2])
            res_len, search_len = list(map(int, msg_lst[-2:]))
            if res_len > 20:
                raise ValueError
            res = get_articles(search, search_len)[:res_len]
        elif msg_lst[-1].isdigit():
            search = ' '.join(msg_lst[:-1])
            res_len = int(msg_lst[-1])
            if res_len > 20:
                raise ValueError
            res = get_articles(search)[:res_len]
        else:
            raise ValueError

        text_msg = '\n\n'.join([f"{i + 1}) [{article['title']}]({article['url']})\n"
                                f"\[лайки: {article['likes']}] \[комментарии: {article['comments']}]"
                                for i, article in enumerate(res)])

        await msg.answer(f'Рузультаты поиска по запросу - {search}:\n\n{text_msg}', parse_mode="Markdown")

    except Exception:
        await msg.answer(f'Упс... чтото не так... \n{help_text}')


if __name__ == '__main__':
    executor.start_polling(dp)
