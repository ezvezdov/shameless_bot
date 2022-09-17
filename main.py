import json
from time import sleep
from os import path
import telebot

# https://github.com/eternnoir/pyTelegramBotAPI
# https://habr.com/ru/post/442800/
# https://xakep.ru/2021/11/28/python-telegram-bots/


with open(path.join('data',"old_data.json"), "w") as outfile:
        json.dump(dict(), outfile)

# create telegram bot
bot = telebot.TeleBot("5617663897:AAF6gy49rlq5lVSNCM2MbZMCUQMSR8WjNO4")
channel_address = "@pausal_delux"

# Add /help command
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Агой камо, крч все просто. Бот должен каждые 5 минут чекать веб шеймлесс на наличие сочных паушальчиков, чтобы с кайфом годьку отработать и пойти спать с кайфом. Бот присылает сообщение только в том случае, если что-то изменилось, добавилась новая смена или кто-то одгласился со старой. Если что-то пошло по пизде перезапусти бота командой /start. Команда /jobs показыает все паушалы, которые есть в данный момент.",parse_mode= 'Markdown')

# Add /jobs command
@bot.message_handler(commands=['jobs'])
def work_list(message):
    import parse_data as pada
    import refactor_data as reda
    import update_data as upda
    pada.generate_data()
    reda.generate_refactored_data()
    upda.update_data()
    bot.send_message(message.chat.id, upda.get_all_works(),parse_mode= 'Markdown')

# Add /start command
@bot.message_handler(commands=['start'])
def send_update(message):
    start = False

    # Add telegram buttons
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=telebot.types.KeyboardButton("/help")
    item2=telebot.types.KeyboardButton("/start")
    item3=telebot.types.KeyboardButton("/jobs")
    markup.add(item1,item2,item3)

    bot.send_message(message.chat.id, "Чус, за паушальчиками пришел, ммм? Советую глянуть раздел /help",reply_markup=markup,parse_mode= 'Markdown')
    import parse_data as pada
    import refactor_data as reda
    import update_data as upda
    while True:
        pada.generate_data()
        reda.generate_refactored_data()
        upda.update_data()
        message_to_send = upda.get_all_works()
        if message_to_send != upda.NO_JOBS_MESSAGE or not start:
            bot.send_message(message.chat.id, message_to_send,parse_mode= 'Markdown')
            start = True
        sleep(60)

    

bot.infinity_polling()