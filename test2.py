import telebot
from telebot import types # для указание типов
#import config
import config

bot = telebot.TeleBot(config.config['token'])



@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("fdjlkg;", url='https://habr.com/ru/all/')
    button2 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)




#bot.polling(none_stop=True)
bot.polling()