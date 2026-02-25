import telebot
from telebot import types
from dotenv import load_dotenv
import datetime
import requests

import meme

import os

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)
user_data = {}

def downloadPhoto(url, user_id):
    response = requests.get(url)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Image/Input/{user_id}_{timestamp}.jpg"
    if user_id not in user_data:
        user_data[user_id] = {}
    with open(filename, 'wb') as file:
        file.write(response.content)
        user_data[user_id]['image_path'] = filename
        user_data[user_id]['status'] = 'waiting_for_text'
    return filename

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сделай мне мем")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Преве. Кароче нажми на кнопк, скинь мне картнк, а потом ткст и я тебе выкину мэм", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def textHandler(message):
    user_id = message.from_user.id
    if message.text == "Сделай мне мем":
        bot.send_message(user_id, "Скинь картинку")
    else:
        memeText = message.text
        print(user_data)
        try:
            if user_data[user_id]:
                meme.applyTextToImage(user_data[user_id]['image_path'], memeText)
                print(user_data[user_id]['image_path'])
                os.remove(user_data[user_id]['image_path'])
                filename = user_data[user_id]['image_path'].split('/')[2]
                with open(f"Image/Output/{filename}_final.jpg", 'rb') as picture:
                    bot.send_photo(user_id, picture)
                user_data.pop(user_id)
            else:
                bot.send_message(user_id, "У меня нет картинки")
        except KeyError:
            bot.send_message(user_id, "Бля бро картнки нет, у меня вообще traceback KeyError")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    file_info = bot.get_file(message.photo[-1].file_id)
    url = f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"
    try:
        user_data['meme_to_send'] = downloadPhoto(url, user_id)
        bot.send_message(user_id, "Картинка у меня! Теперь скинь ткст")
    except Exception(e):
        bot.send_message(user_id, "БЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ")

bot.polling(none_stop=True, interval=0)