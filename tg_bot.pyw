from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink, hspoiler
from config import telegram_token
from aiogram.dispatcher.filters import Text
import pandas as pd
import numpy as np


bot = Bot(token=telegram_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    buttons = ['Send a secret word', 'Random movie']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    print(keyboard)
    await message.answer('Enjoy our news', reply_markup=keyboard)


@dp.message_handler(Text(equals="Send a secret word"))
async def secretword(message: types.Message):
    await message.reply("Secret answer!")


# Show a movie
@dp.message_handler(Text(equals="Random movie"))
async def get_all_news(message: types.Message):

    # Read a csv file and create random number.
    file = pd.read_csv('./.data/netflix_titles.csv')
    file_len = file[file.columns[0]].count() - 1
    random_value = np.random.randint(0, file_len)

    # # Message view with html markdown.
    # news = f"<b>{file['title'][random_value]}</b> " \
    #        f"({file['release_year'][random_value]})\n" \
    #        f"{file['description'][random_value]}"

    # Message view with aiogram markdown.
    news = f"{hbold(file['title'][random_value])} " \
           f"({file['release_year'][random_value]})\n" \
           f"{file['description'][random_value]}"

    await message.answer(news)



if __name__ == '__main__':
    print('It is working!')
    executor.start_polling(dp, skip_updates=True)