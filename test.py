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
    msg = bot.send_message(message.chat.id, "Запись данных...")
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Данные записаны!!!")

bot.infinity_polling(none_stop=True)