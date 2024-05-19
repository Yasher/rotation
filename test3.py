import telebot
from telebot import types # для указание типов
#import config
import config

bot = telebot.TeleBot(config.config['token'])



@bot.message_handler(commands=['start'])
def selfmyself(message):
    service = telebot.types.ReplyKeyboardMarkup(True, True)
    service.row('Wunderlist')
    service.row('Telegraph')
    service.row('Погода')
    bot.send_message(message.from_user.id, 'Что будем делать?', reply_markup=service)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Wunderlist":
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Что', reply_markup=a)

bot.polling(none_stop=True)