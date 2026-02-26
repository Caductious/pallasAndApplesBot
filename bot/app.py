import telebot
from telebot import types
from dotenv import load_dotenv
import datetime
import requests

import meme

import os
import time

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)
user_data = {}

def downloadPhoto(url, user_id):
    response = requests.get(url)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Image/Input/{user_id}_{timestamp}.jpg"

    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def send_meme(user_id):
    with open(user_data[user_id]['final_path'], 'rb') as picture:
        bot.send_photo(user_id, picture)

    with open("log.txt", "a") as log:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log.write(f"{now};send_photo;{user_id};meme;success\n")

    return 'sent'

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
        try:
            if user_data[user_id]['status'] == 'waiting_for_text':

                user_data[user_id]['memeText'] = message.text
                user_data[user_id]['memeText'] = user_data[user_id]['memeText'].replace("\n", " ")
                with open("log.txt", "a") as log:
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    log.write(f"{now};text_message;{user_id};{user_data[user_id]['memeText']};success\n")    

                user_data[user_id]['final_path'] = meme.applyTextToImage(user_data[user_id]['source_path'], user_data[user_id]['memeText'])
                user_data[user_id]['status']= 'ready'

                user_data[user_id]['attempts'] = 1
                while user_data[user_id]['status'] == 'ready' and user_data[user_id]['attempts'] <= 10:
                    try:
                        user_data[user_id]['status'] = send_meme(user_id)
                        break

                    except requests.exceptions.ConnectionError:
                        bot.send_message(user_id, f"Траблы с инетом, попытка {user_data[user_id]['attempts']}/10")
                        user_data[user_id]['attempts']+=1
                        time.sleep(10)
                        with open("log.txt", "a") as log:
                            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            log.write(f"{now};send_photo;{user_id};meme;internet_fail\n")
                        if user_data[user_id]['attempts'] == 10 and user_data[user_id]['status'] != 'sent':
                            os.remove(user_data[user_id]['source_path'])
                            os.remove(user_data[user_id]['final_path'])
                            user_data.pop(user_id)
                            bot.send_message(user_id, "Попробуйте пожалуйста снова я вас подвёл")
                if user_data[user_id]['status'] == "sent":
                    os.remove(user_data[user_id]['source_path'])
                    os.remove(user_data[user_id]['final_path'])
                    user_data.pop(user_id)

                    
        except KeyError:
            bot.send_message(user_id, "Картнки нет, нет и мема")
    


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    file_info = bot.get_file(message.photo[-1].file_id)
    url = f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['satus'] = "waiting"
    user_data[user_id]['attempts'] = 1
    while user_data[user_id]['satus'] == "waiting" and user_data[user_id]['attempts'] <= 10:
        try:
            user_data[user_id]['source_path']  = downloadPhoto(url, user_id)
            bot.send_message(user_id, "Картинка у меня! Теперь скинь текст")
            user_data[user_id]['status'] = 'waiting_for_text'
            with open("log.txt", "a") as log:
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                log.write(f"{now};download_photo;{user_id};{url};success\n")
            break
        except requests.exceptions.ReadTimeout:
            bot.send_message(user_id, f"Траблы с инетом, попытка {user_data[user_id]['attempts']}/10")
            user_data[user_id]['attempts'] += 1
            time.sleep(10)
            with open("log.txt", "a") as log:
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                log.write(f"{now};download_photo;{user_id};{url};timeOutError\n")
            if user_data[user_id]['attempts'] == 10 and user_data[user_id]['status'] != 'waiting_for_text':
                os.remove(user_data[user_id]['source_path'])
                os.remove(user_data[user_id]['final_path'])
                user_data.pop(user_id)
                bot.send_message(user_id, "Попробуйте пожалуйста снова я вас подвёл")
        

bot.polling(none_stop=True, interval=0)