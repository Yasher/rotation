#age = 66

#print ("hkjdfghk" + str(age) +"jfadh")

import telebot
from telebot import types # для указание типов
import config
#import config
import config

bot = telebot.TeleBot(config.config['token'])




#@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(commands=['start']) #создаем команду
#def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")

def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    markup.add(button1)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)



bot.infinity_polling(none_stop=True)