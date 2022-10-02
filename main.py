import json
from time import sleep
from os import path, remove
import telebot
from telebot import types
from datetime import datetime

# https://github.com/eternnoir/pyTelegramBotAPI
# https://habr.com/ru/post/442800/
# https://xakep.ru/2021/11/28/python-telegram-bots/


with open(path.join('data',"old_data.json"), "w") as outfile:
        json.dump(dict(), outfile)

logfile = open(path.join('data',"log.txt"), "w")

# create telegram bot
bot = telebot.TeleBot("5617663897:AAF6gy49rlq5lVSNCM2MbZMCUQMSR8WjNO4")
channel_address = "@pausal_delux"

is_bot_working = True
refresh_frequency = 60 # in seconds
is_bot_started = False
start_time = 0


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

@bot.message_handler(commands=['info'])
def send_info_message(message):
    message_to_send = ""
    global is_bot_working, refresh_frequency, start_time
    message_to_send += "*Состояние*: працуе\n" if is_bot_working else "*Состояние*: непрацуе\n"
    message_to_send = message_to_send + "*Время работы*: " + strfdelta(datetime.now() - start_time,"{days} дней, {hours}:{minutes}:{seconds}\n")
    message_to_send = message_to_send + "*Частота обновления*: " + str(refresh_frequency) + " секунд\n"
    bot.send_message(message.chat.id, message_to_send,parse_mode= 'Markdown')
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEYWOBjLNdmC5dclv0jBbXmPPlpUa-q_AACChIAAs0C6EvjoLPI5axr9CkE")
    

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    
    d["hours"] = format(d["hours"], '02d')
    d["minutes"] = format(d["minutes"], '02d')
    d["seconds"] = format(d["seconds"], '02d')
    return fmt.format(**d)


# Add /stop command
@bot.message_handler(commands=['stop'])
def stop_bot(message):
    try: remove(path.join("data","parsed_data.json"))
    except: pass
    try: remove(path.join("data","refactored_data.json"))
    except: pass
    global is_bot_working
    is_bot_working = False
    bot.send_message(message.chat.id, "Чус бус автобус. I'll be  back 😎",parse_mode= 'Markdown')
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEYWM5jLNUtmN7S293meV95TtQQn61L3gAC3BIAAvMNqUj9BaNVQlopLikE')

@bot.message_handler(commands=['continue'])
def stop_bot(message):
    global is_bot_working
    is_bot_working = True
    bot.send_message(message.chat.id, "Я же говорил, что вернусь 😎",parse_mode= 'Markdown')

# Add /start command
@bot.message_handler(commands=['start'])
def send_update(message):
    global is_bot_started,is_bot_working,start_time
    if is_bot_started:
        bot.send_message(message.chat.id, "Зачем меня запускать, если я уже запущен 🤨",parse_mode= 'Markdown')
        return
    # global is_bot_working
    is_bot_working = True
    # global start_time
    start_time = datetime.now()

    # Add telegram buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help_button = types.KeyboardButton("/help")
    start_button = types.KeyboardButton("/start")
    stop_button = types.KeyboardButton("/stop")
    jobs_button = types.KeyboardButton("/jobs")
    info_button = types.KeyboardButton("/info")
    continue_button = types.KeyboardButton("/continue")
    markup.add(help_button,start_button,stop_button,continue_button,info_button,jobs_button)

    bot.send_message(message.chat.id, "Чус, за паушальчиками пришел, ммм? Советую глянуть раздел /help",reply_markup=markup,parse_mode= 'Markdown')
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAEYWNxjLNaqnB_SFteoZArPZxE8VwKyMgACBBcAAs_q6UvdZbGbN2nnbikE")
    
    import parse_data as pada
    import refactor_data as reda
    import update_data as upda
    while True:
        global refresh_frequency
        if is_bot_working:
            try:
                pada.generate_data()
            except Exception as e:
                bot.send_message(message.chat.id, "Короче, произошла какая-то залупа с синхронизацией с сервером шеймлесс. Работа бота может быть ограничена. Текст ошибки \'" + e + "\'.",reply_markup=markup,parse_mode= 'Markdown')
            reda.generate_refactored_data()
            upda.update_data()
            message_to_send = upda.get_new_works()
            if message_to_send != upda.NO_JOBS_MESSAGE or not is_bot_started:
                bot.send_message(message.chat.id, message_to_send,parse_mode= 'Markdown')
                is_bot_started = True
        sleep(refresh_frequency)

    

bot.infinity_polling()

