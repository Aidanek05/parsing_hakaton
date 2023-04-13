import telebot
import json
from telebot import types
from decouple import config

from parse import main, get_description, today

TOKEN = config("TOKEN")

BOT = telebot.TeleBot(TOKEN)

def get_keyboard():
    kboard = types.InlineKeyboardMarkup()
    with open(f'news_{today}.json', 'r') as  file:
        for number, news in enumerate(json.load(file)):
            kboard.add(
                types.InlineKeyboardButton(
                text=news['title'],
                callback_data=str(number)
                )
            )
    return kboard




@BOT.message_handler(commands=['start', 'hi'])
def start(message):
    main()
    BOT.send_message(message.chat.id, f'Привет {message.from_user.first_name}!  Новоти на сегодня', reply_markup=get_keyboard)

    BOT.callback_querry_handler(func=lambda callback: True)
    def send_news(callback):
        with open(f'news__{today},json', 'r') as file:
            news = json.load(file)[int(callback)]
            text = f'{news["title"]} \n{get_description(news["news_link"])} \n {news["photo"]} '
        BOT.send_message(callback.message.chat.id, text=text)


BOT.polling(none_stop=True, interval=0)